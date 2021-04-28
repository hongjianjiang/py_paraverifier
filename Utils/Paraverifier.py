# Author: Hongjian Jiang

import os
import json
from type import *
from smt2 import *
from invHold import *
from parse import *

GUARD, PRE, INV = range(3)
file = '../Protocol/n_mutualEx.json'

def convert_hint_type(s):
    if s == "GUARD":
        return GUARD
    elif s == "PRE":
        return PRE
    elif s == "INV":
        return INV
    else:
        raise NotImplementedError


class ParaSystem():
    """Describes a parametrized system. The system consists of:
    name: name of the system.
    vars: list of variables.
    states: list of states, assumed to be distinct.
    rules: list of rules.
    invs: list of invariants.
    """
    def __init__(self, name, vars, states, rules, invs):
        self.name = name
        self.vars = vars
        self.states = states
        self.rules = rules
        self.invs = invs

        self.allinvs = []

        # var_map used in gcl library
        self.var_map = dict()
        for i, v in enumerate(self.vars):
            self.var_map[v] = i

        # state_map
        self.state_map = dict()
        for i, state in enumerate(self.states):
            self.state_map[state] = i

    def __str__(self):
        res = "Variables: " + ", ".join(v.name for v in self.vars) + "\n"

        res += "States: " + ", ".join(str(v) for v in self.states) + "\n"

        res += "Number of rules: %d\n" % len(self.rules)
        for i, rule in enumerate(self.rules):
            res += "%d: guard: %s assign: %s\n" % (i, str(rule.getStatement()),str(rule.getGuard()))

        res += "Number of invariants: %d\n" % len(self.invs)
        for i, inv in enumerate(self.invs):
            inv_term = inv
            res += "%d: %s" % (i, str(inv_term)) + "\n"

        return res

    def replace_states(self, t):
        """Replace states by their corresponding numbers."""
        if t in self.states:
            return Nat(self.state_map[t])
        elif t.is_comb():
            return self.replace_states(t.fun)(self.replace_states(t.arg))
        else:
            return t

    def get_subgoal(self, inv_id, rule_id, case_id, hint):
        """Obtain the subgoal for the given case and hint.

        inv_id: index of the invariant to be shown at the end of the
                transition.
        rule_id: index of the transition rule.
        case_id: index of the case. The cases are as follows:
            - 0 to n-1: parameter in rule equals i'th parameter in inv.
            - n: parameter in rule does not equal any parameter in inv.
        hint: either:
            - GUARD: invariant is implied by the guard.
            - PRE: invariant is implied by the same invariant in the
                   previous state.
            - INV, i, inst:
                Invariant is implied by the guard and a different
                invariant i in the previous state. inst is a list specifying
                how to instantiate the invariant.

        """
        rule_var, guard, assigns = self.rules[rule_id]
        inv_vars, inv = self.invs[inv_id]
        assert case_id >= 0 and case_id <= len(inv_vars), \
               "get_subgoal: unexpected case_id."

        # Obtain invariant on the updated state.
        def subst(t):
            if t.is_comb() and t.fun in self.vars and t.arg in inv_vars:
                # Substitution for a parameterized variable
                if case_id < len(inv_vars) and inv_vars[case_id] == t.arg and \
                   t.fun(rule_var) in assigns:
                    return assigns[t.fun(rule_var)]
                elif t.fun in assigns:
                    return assigns[t.fun](t.arg)
                else:
                    return t
            elif t.is_var():
                # Substitution for a non-parameterized variable
                if t in assigns:
                    return assigns[t]
                else:
                    return t
            elif t.is_const():
                return t
            elif t.is_comb():
                return subst(t.fun)(subst(t.arg))
            else:
                raise NotImplementedError

        inv_after = subst(inv)
        if hint == GUARD:
            return Implies(guard, inv_after)
        elif hint == PRE:
            return Implies(inv, inv_after)
        else:
            hint_ty, hint_inv_id, subst_vars = hint
            if hint_ty == INV:
                inv_vars, inv = self.invs[hint_inv_id]
                inv_var_nms = [v.name for v in inv_vars]
                subst = Inst((nm, Var(subst_var, NatType)) for nm, subst_var in zip(inv_var_nms, subst_vars))
                inv_subst = inv.subst(subst)
                return Implies(inv_subst, guard, inv_after)

    def verify_subgoal(self, inv_id, rule_id, case_id, hint):
        """Verify the subgoal from the given hints.

        In addition to the assumptions given in get_subgoal, we need
        some additional assumptions, including distinctness of states.

        """
        goal = self.get_subgoal(inv_id, rule_id, case_id, hint)
        goal = self.replace_states(goal)
        if z3wrapper.z3_loaded:
            ans = z3wrapper.solve(goal)
        else:
            ans = True
        return goal, ans

    def add_invariant_prop(self):
        """Add the invariant for the system in GCL."""
        for inv in self.invs:
            # print(inv)
            formula = inv.getInv()
            self.allinvs.append(str(formula))
        return self.allinvs

    def search_invariant(self):
        for inv in self.allinvs:
            for r in self.rules:
                statement = r.getStatement()
                if invHoldCondition(statement,parse_form(inv),file) == 3:
                    print("test:")
                    print(parse_form(inv))
                    newInv=invHoldForCondition3(r.getGuard(),inv)
                    print("newInv:",newInv)
                    self.allinvs.append(newInv)

def load_system(filename):
    dn = os.path.dirname(os.getcwd())
    with open(os.path.join(dn, 'Protocol/' + filename + '.json'), encoding='utf-8') as a:
        data = json.load(a)
    print(data)
    name = data['name']
    vars = []
    for key, value in data['vars'].items():
        T = parse_vars(key)
        vars.append(T)
    states = []
    for i, nm in enumerate(data['states']):
        T = parse_state(nm)
        states.append(T)
    rules = []
    for r in data['rules']:
        T = parse_rule(str(r))
        rules.append(T)
    invs = []
    for inv in data['invs']:
        T = parse_prop(str(inv))
        invs.append(T)
    # print(ParaSystem(name, vars, states, rules, invs))
    return ParaSystem(name, vars, states, rules, invs)


if __name__ == '__main__':
    p = load_system('n_mutualEx')
    p.add_invariant_prop()
    p.search_invariant()
