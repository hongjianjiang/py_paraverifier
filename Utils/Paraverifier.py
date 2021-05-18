# Author: Hongjian Jiang

import os
from Utils.invHold import *
from Utils.parse import *
from Utils.smt2 import *
file = '../Protocol/n_mutual.json'


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
    T = parse_init(str(init))
    inits.append(T)
    return ParaSystem(name, vars, states, rules, invs, inits)


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
        self.allinvs = [] # store the whole invariant formula
        self.foundedinvs = [] # store the founded invariant formula
        self.relation = {}
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
        '''
        :return: the founed invariant
        '''
        newInv = []
        print(self.allinvs)
        for inv in self.invs:
            for r in self.rules:
                statement = r.getStatement()
                if invHoldCondition(statement,inv.getInv(),file) == 3:
                    if invHoldForCondition3(r.getGuard(),weakestprecondition(statement,inv.getInv())) not in newInv:
                        newStr = invHoldForCondition3(r.getGuard(),weakestprecondition(statement,inv.getInv()))
                        temp = self.smt2.getStringInFormula(newStr)
                        formula_list = temp.split('&')
                        list1 = []
                        for f in formula_list:
                            if self.smt2.getEqualFirst(f).strip() != self.smt2.getEqualSecond(f).strip():
                                list1.append(f.strip())
                        newStr = '~('+" & ".join(list1)+')'
                        newInv.append(newStr)
                        if newStr not in self.foundedinvs:
                            self.foundedinvs.append(newStr)
                        if newStr not in self.allinvs:
                            self.allinvs.append(newStr)
            self.relation[str(inv.getInv())] = newInv
        return newInv

    def searchInvFromGivenFormula(self,form):
        '''
        :param form: the given candidate formula
        :return: the new founded invariant set
        '''
        newInv = []
        print(form)
        for r in self.rules:
            statement = r.getStatement()
            if invHoldCondition(statement, parse_form(form), file) == 3:
                if invHoldForCondition3(r.getGuard(), weakestprecondition(statement, parse_form(form))) not in newInv:
                    newStr = invHoldForCondition3(r.getGuard(), weakestprecondition(statement, parse_form(form)))
                    temp = self.smt2.getStringInFormula(newStr)
                    formula_list = temp.split('&')
                    list1 = []
                    for f in formula_list:
                        if self.smt2.getEqualFirst(f).strip() != self.smt2.getEqualSecond(f).strip():
                            list1.append(f.strip())
                    newStr = '~(' + " & ".join(list1) + ')'
                    newInv.append(newStr)
                    if newStr not in self.foundedinvs:
                        self.foundedinvs.append(newStr)
                    if newStr not in self.allinvs:
                        self.allinvs.append(newStr)
        self.relation[form] = newInv
        return newInv

    def judgeInv(self, inv):
        '''
        :param inv:
        :return: the count of invhold1 and invhold3
        '''
        cinv1, cinv3 = 0, 0
        for r in self.rules:
            statement = r.getStatement()
            if invHoldCondition(statement,parse_form(inv),file) == 1:
                cinv1 = cinv1 + 1
            elif invHoldCondition(statement,parse_form(inv),file) == 3:
                cinv3 = cinv3 + 1
        return (cinv1, cinv3)

    def judgeGuard2Formula(self,inv):
        formula = re.findall(r'[(](.*)[)]', inv, re.S)[0]
        fl = []
        for i in formula.split('&'):
            fl.append(i.strip())
        for r in self.rules:
            gl = []
            guard = str(r.getGuard())
            if '(' in guard:
                guard = re.findall(r'[(](.*)[)]', guard, re.S)[0]
            for i in guard.split('&'):
                gl.append(i.strip())
            print('fl:',fl,'gl:',gl)
            if len(gl) == len(fl):
                flag = True
                for i in fl:
                    if i not in gl:
                        print(i)
                        flag = False
                if flag != False:
                    return True
        return False



if __name__ == '__main__':
    p = load_system('n_mutual.json')
    print(p.judgeGuard2Formula('~(x=True & n j=T)'))
    # p.add_invariant_prop()
    # print("new inv:", p.search_invariant())
    # print(p.allinvs)
    # print(p.foundedinvs)
    # print(p.searchInvFromGivenFormula('n i =E & x = True'))
    # print(p.relation)
