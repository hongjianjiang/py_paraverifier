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

    def add_invariant_prop(self):
        """Add the invariant for the system in GCL."""
        for inv in self.invs:
            # print(inv)
            formula = inv.getInv()
            self.allinvs.append(str(formula))
        print(self.allinvs)
        return self.allinvs

    def search_invariant(self):
        for inv in self.allinvs:
            for r in self.rules:
                statement = r.getStatement()
                if invHoldCondition(statement,parse_form(inv),file) == 3:
                    newInv=invHoldForCondition3(r.getGuard(),inv)
                    #nusmv simpify
                    print("newInv:",newInv)
                    self.allinvs.append(newInv)
# inv: ~(n[i]=T & (x=True & (n[i]=C & n[j]=C)))
def load_system(filename):
    dn = os.path.dirname(os.getcwd())
    with open(os.path.join(dn, 'Protocol/' + filename + '.json'), encoding='utf-8') as a:
        data = json.load(a)
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
