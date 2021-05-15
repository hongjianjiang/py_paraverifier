# Author: Hongjian Jiang

import os
from Utils.invHold import *
from Utils.parse import *
from Utils.smt2 import *
file = '../Protocol/n_mutual.json'


class ParaSystem():
    """Describes a parametrized system. The system consists of:
    name: name of the system.
    vars: list of variables.
    states: list of states, assumed to be distinct.
    rules: list of rules.
    invs: list of invariants.
    init: initial state.
    """
    def __init__(self, name, vars, states, rules, invs, init):
        self.name = name
        self.vars = vars
        self.states = states
        self.rules = rules
        self.invs = invs
        self.init = init
        self.allinvs = []
        self.smt2 = SMT2(file)

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

        res += "Initial States: \n"
        for i, inv in enumerate(self.init):
            inv_term = inv
            res += "%d: %s" % (i, str(inv_term)) + "\n"

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
            formula = inv.getInv()
            self.allinvs.append(str(formula))
        return self.allinvs

    def search_invariant(self):
        newInv = []
        for inv in self.allinvs:
            for r in self.rules:
                statement = r.getStatement()
                if invHoldCondition(statement,parse_form(inv),file) == 3:
                    if invHoldForCondition3(r.getGuard(),weakestprecondition(statement,parse_form(inv))) not in newInv:
                        newStr = invHoldForCondition3(r.getGuard(),weakestprecondition(statement,parse_form(inv)))
                        temp = self.smt2.getStringInFormula(newStr)
                        formula_list = temp.split('&')
                        for f in formula_list:
                            # print('test1:',self.smt2.getEqualFirst(f).strip()==self.smt2.getEqualSecond(f).strip(),self.smt2.getEqualFirst(f),self.smt2.getEqualSecond(f))
                            if self.smt2.getEqualFirst(f).strip()==self.smt2.getEqualSecond(f).strip():
                                print('test2')
                                formula_list.remove(f)
                        newStr = '~('+" & ".join(formula_list)+')'
                        newInv.append(newStr)
        return newInv

    def judgeInv(self,inv):
        for r in self.rules:
            statement = r.getStatement()
            print('r:',r.getStatement())
            print("wp:",weakestprecondition(statement,parse_form(inv)))
            if invHoldCondition(statement,parse_form(inv),file) == 1:
                return True
        return False


def load_system(filename):
    dn = os.path.dirname(os.getcwd())
    with open(os.path.join(dn, 'Protocol/' + filename), encoding='utf-8') as a:
    # with open(filename, encoding='utf-8') as a:
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
    invs = []
    for inv in data['invs']:
        T = parse_prop(str(inv))
        for new in T.getArgs()[0]:
            for r in data['rules']:
                r['var'] = str(r['var']).replace("i", new)
                r['guard'] = str(r['guard']).replace("i", new)
                for k in r['assign'].keys():
                    if 'i' in k and new != 'i':
                        new1 = str(k).replace("i", new)
                        r['assign'][new1] = r['assign'][k]
                        del r['assign'][k]
                T1 = parse_rule(str(r))
                rules.append(T1)

        for r in data['rules']:
            r['var'] = str(r['var']).replace(T.getArgs()[0][-1], "k")
            r['guard'] = str(r['guard']).replace(T.getArgs()[0][-1], "k")
            for k in r['assign'].keys():
                if T.getArgs()[0][-1] in k:
                    new1 = str(k).replace(T.getArgs()[0][-1], "k")
                    r['assign'][new1] = r['assign'][k]
                    del r['assign'][k]
            T2 = parse_rule(str(r))
            rules.append(T2)
        invs.append(T)
    inits = []
    init = data['init']
    # print(init)
    T = parse_init(str(init))
    inits.append(T)
    # print(ParaSystem(name, vars, states, rules, invs, inits))
    return ParaSystem(name, vars, states, rules, invs, inits)


if __name__ == '__main__':
    p = load_system('n_mutual.json')
    p.add_invariant_prop()
    print(p.allinvs)
    print("new inv:", p.search_invariant())
    # for i in p.init:
    #     print(i.getFormula())

