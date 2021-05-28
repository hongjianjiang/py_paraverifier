# Author: Hongjian Jiang

import os
from invHold import *
from parse import *
from smt2 import *
import json
import os
import numpy as np
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
        states.append(nm)
    rules = []
    invs = []
    for inv in data['invs']:
        T = parse_prop(str(inv))
        invs.append(T)
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

        # for r in data['rules']:
        #     r['var'] = str(r['var']).replace(T.getArgs()[0][-1], "k")
        #     r['guard'] = str(r['guard']).replace(T.getArgs()[0][-1], "k")
        #     for k in r['assign'].keys():
        #         if T.getArgs()[0][-1] in k:
        #             new1 = str(k).replace(T.getArgs()[0][-1], "k")
        #             r['assign'][new1] = r['assign'][k]
        #             del r['assign'][k]
        #     T2 = parse_rule(str(r))
        #     rules.append(T2)
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
        self.invForm = []
        self.allinvs = [] # store the whole invariant formula
        self.foundedinvs = [] # store the founded invariant formula
        self.relation = {}
        self.smt2 = SMT2(file)
        self.search_flag = dict()
        self.add_invariant_prop()
        self.search_invariant1()
        # var_map used in gcl library
        self.var_map = dict()
        for i, v in enumerate(self.vars):
            self.var_map[v] = i
        # state_map
        self.state_map = dict()
        for i, state in enumerate(self.states):
            self.state_map[state] = i
        self.max = self.getMaxValue()

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

    def getMaxValue(self):
        max = 0
        for i, k in self.relation.items():
            for j in k:
                result = re.findall(r'~\((.*)\)', j, re.S)[0]
                if max < len(result.split('&')):
                    max = len(result.split('&'))
        return max

    def add_invariant_prop(self):
        """Add the invariant for the system in GCL."""
        for inv in self.invs:
            formula = inv.getInv()
            self.invForm.append(str(formula))
            self.allinvs.append(str(formula))
            self.search_flag[str(formula)] = False
        return self.allinvs

    # def search_invariant(self):
    #     '''
    #     :return: the founed invariant
    #     '''
    #     newInv = []
    #     for inv in self.invs:
    #         for r in self.rules:
    #             statement = r.getStatement()
    #             if invHoldCondition(statement, inv.getInv(), file) == 3: #inv.getInv()
    #                 if invHoldForCondition3(r.getGuard(), weakestprecondition(statement, inv.getInv())) not in newInv:
    #                     newStr = invHoldForCondition3(r.getGuard(), weakestprecondition(statement, inv.getInv()))
    #                     temp = self.smt2.getStringInFormula(newStr).replace('(','').replace(')','')
    #                     print('tp',temp)
    #                     formula_list = temp.split('&')
    #                     list1 = []
    #                     print('fs:', formula_list)
    #                     for f in formula_list:
    #                         if self.smt2.getEqualFirst(f).strip() != self.smt2.getEqualSecond(f).strip():
    #                             list1.append(f.strip())
    #                     newStr = '~('+" & ".join(list1)+')'
    #                     newInv.append(newStr)
    #                     if newStr not in self.foundedinvs:
    #                         self.foundedinvs.append(newStr)
    #                     if newStr not in self.allinvs:
    #                         self.allinvs.append(newStr)
    #         self.relation[str(inv.getInv())] = newInv
    #
    #     return newInv

    def search_invariant1(self):
        '''
        :return: the founed invariant
        '''
        # print(self.allinvs)
        if os.path.exists('../Data/'+self.name + '_data.json'):
            with open('../Data/'+self.name + '_data.json', 'r', encoding='utf8') as fp:
                fp = json.load(fp)
                self.relation = fp['relation']
                self.allinvs = fp['allinvs']
                self.foundedinvs = fp['foundedinvs']
        else:
            for inv in self.allinvs:#self.invs:
                if self.search_flag[inv]:
                    continue
                else:
                    # print('inv has not been explored..')
                    newInv = []
                    for r in self.rules:
                        statement = r.getStatement()
                        if invHoldCondition(statement, parse_form(inv), file) == 3: #inv.getInv()
                            newStr = invHoldForCondition3(r.getGuard(), weakestprecondition(statement, parse_form(inv)))
                            if newStr not in newInv:
                                temp = self.smt2.getStringInFormula(newStr).replace('(','').replace(')','')
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
                                    self.search_flag[newStr] = False
                    self.relation[inv] = newInv
                    # newInv = []
                    self.search_flag[inv] = True
                # for key, value in self.relation.items():
                print(len(self.relation))
            dict = {'relation': self.relation, 'allinvs' : self.allinvs, 'foundedinvs' : self.foundedinvs}
            jsObj = json.dumps(dict)
            fileObject = open('../Data/'+self.name+ '_data.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()

    def searchInvFromGivenFormula(self,form):
        '''
        :param form: the given candidate formula
        :return: the new founded invariant set
        '''
        newInv = []
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
        '''
        :param inv:
        :return: the result that the guard can imply the inv formula
        '''
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
            if len(gl) == len(fl):
                flag = False
                for i in fl:
                    if i not in gl:
                        flag = True
                if flag == False:
                    return True
        return False

    def initSatInv(self,inv):
        str_init = ''
        for i in self.init:
            str_init += ' & ' + (i.getFormula().replace('(','').replace(')',''))
        # print('~('+self.smt2.getStringInFormula(inv) + str_init+')')
        return self.smt2.check('~('+self.smt2.getStringInFormula(inv) + str_init+')')


    def transform2onehot(self, formula):
        str1 = re.findall(r'~\((.*)\)',formula,re.S)[0]
        slen = len(self.states)*2 + 2
        list1 = []
        for i in self.states:
            str = 'n i='+i
            list1.append(str)
        for i in self.states:
            str = 'n j='+i
            list1.append(str)
        list1.append('x=True')
        list1.append('x=False')
        slist = str1.split('&')
        temp = []
        for i in slist:
            temp.append(i.strip())
        list2 = []
        for i in temp:
            list2.append(list1.index(i))
        n = np.zeros(slen)
        for i in list2:
            n[i] = 1
        return n


if __name__ == '__main__':
    p = load_system('n_mutual.json')
    # print(p.add_invariant_prop())
    # for i,k in p.relation.items():
    #     print(i,'->',k)
    # print('===========================')
    # for i in p.allinvs:
        # print(i)
    # p.search_invariant1()
    # print(p.foundedinvs)
    # print(p.relation['~(n i=C & n j=C)'])
    # print(p.relation)
    list = ['~(n i=C & n k=E & n j=C)', '~(n j=T & x=True & n k=E & n i=E)', '~(n k=C & n j=C & n i=E)']
    # print(p.transform2onehot('~(n j=T & x=True)').astype(dtype=np.float32))
    print(p.searchInvFromGivenFormula('~(n j=C)'))
    # for i, k in p.relation.items():
    #     for j in k:
    #         print(j)

# [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
# action: 0
# ~(n i=I & x=True) 3
# ~(x=True)
# nfs: ['~(n i=E & (True=True)', '~(n j=E & (True=True)']