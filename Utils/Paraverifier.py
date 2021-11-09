# Author: Hongjian Jiang

from Utils.invHold import *
from Utils.parse import *
from Utils.smt2 import *
import json
import os
import numpy as np
from numpy import *
file = '../Protocol/n_mutual.json'
import math



def load_system(filename):
    dn = os.path.dirname(os.getcwd())
    with open(os.path.join(dn, 'Protocol/' + filename), encoding='utf-8') as a:
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
                guard = str(r['guard'])
                templist1 = guard.split('&')
                varlist = []
                valuelist = []
                for i in templist1:
                    varlist.append(re.findall(r'(.*?)\s*=', i, re.S)[0].strip())
                    valuelist.append(re.findall(r'=\s*(.*)', i, re.S)[0].strip())
                for i in varlist:
                    varlist[varlist.index(i)] = varlist[varlist.index(i)].replace('i', new)
                guardStr = ''
                for i in range(len(varlist)):
                    if i != len(varlist)-1:
                        guardStr += varlist[i] + ' = ' + valuelist[i] + ' & '
                    else:
                        guardStr += varlist[i] + ' = ' + valuelist[i]
                r['guard'] = guardStr
                for k in r['assign'].keys():
                    if 'i' in k and new != 'i':
                        new1 = str(k).replace("i", new)
                        r['assign'][new1] = r['assign'][k]
                        del r['assign'][k]
                T1 = parse_rule(str(r))
                rules.append(T1)
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
        self.relation = {}
        self.smt2 = SMT2(file)
        self.search_flag = dict()
        self.add_invariant_prop()
        self.search_invariant1()
        self.mapping = []
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

    def search_invariant1(self):
        '''
        :return: the founed invariant
        '''
        relation = {}
        if os.path.exists('../Data/'+self.name + '_data.json'):
            with open('../Data/'+self.name + '_data.json', 'r', encoding='utf8') as fp:
                fp = json.load(fp)
                self.relation = fp['relation']
                self.allinvs = fp['allinvs']
        else:
            for inv in self.allinvs:
                #self.invs:
                if self.search_flag[inv]:
                    continue
                else:
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
                                newStr = '~' + '(' + " & ".join(list(set(list1))).replace('(', '').replace(')',
                                                                                                           '') + ')'
                                if not newInv and not self.judgeTrueOfForm(newStr):
                                    newInv.append(newStr)
                                else:
                                    for i in newInv:
                                        if not self.judgeExistSameFormula(i, newStr) and not self.judgeTrueOfForm(
                                                newStr):
                                            newInv.append(newStr)
                                print('new:', newStr, '---->', r.getGuard(), '---->',
                                      weakestprecondition(statement, parse_form(inv)))

                    for f in newInv:
                        str1 = self.normalize(f)
                        if str1 not in self.allinvs.copy():
                            self.allinvs.append(str1)
                            self.search_flag[str1] = False
                relation[inv] = newInv
            self.allinvs = self.removeSamePatInList(self.allinvs)
            for i in self.allinvs:
                self.relation[i] = relation[i]
            dict = {'relation': self.relation, 'allinvs': self.allinvs}
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
                    temp = temp.replace('(', '').replace(')', '')
                    formula_list = temp.split('&')
                    list1 = []
                    for f in list(set(formula_list)):
                        if self.smt2.getEqualFirst(f).strip() != self.smt2.getEqualSecond(f).strip():
                            list1.append(f.strip())

                    newStr = '~'+'('+" & ".join(list(set(list1))).replace('(', '').replace(')', '')+')'
                    if not newInv and not self.judgeTrueOfForm(newStr):
                        newInv.append(newStr)
                    else:
                        for i in newInv:
                            if not self.judgeExistSameFormula(i, newStr) and not self.judgeTrueOfForm(newStr):
                                newInv.append(newStr)
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

    def judgeGuard2Formula(self, inv):
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
                if not flag:
                    return True
        return False

    def initSatInv(self, inv):
        str_init = ''
        for i in self.init:
            str_init += ' & ' + (i.getFormula().replace('(','').replace(')',''))
        return self.smt2.check('~('+self.smt2.getStringInFormula(inv) + str_init+')')

    def transform2onehot(self, formula):
        str1 = re.findall(r'~\((.*)\)', formula, re.S)[0]
        slen = len(self.states)*2 + 2
        list1 = []
        for i in self.states:
            str = 'n i='+i
            list1.append(str)
            self.mapping.append(str)
        for i in self.states:
            str = 'n j='+i
            list1.append(str)
            self.mapping.append(str)
        list1.append('x=True')
        self.mapping.append('x=True')
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

    def transformlist2onehot(self,list):
        l = []
        for i in list:
            l.append(self.transform2onehot(i))
        return np.asarray(l)

    def converhot2list(self,np):
        rlist = []
        for i in np.astype(int):
            list = []
            for j in range(len(i)):
                if i[j] == 1:
                    list.append(self.mapping[j])
            str = '~('+' & '.join(list)+')'
            rlist.append(str)
        return rlist

    def judgeExistSameFormula(self, form1, form2):
        str1 = re.findall(r'~\((.*)\)', form1, re.S)[0]
        str2 = re.findall(r'~\((.*)\)', form2, re.S)[0]
        list1 = str1.split('&')
        list2 = str2.split('&')
        flist1 = []
        flist2 = []
        for i in list1:
            flist1.append(i.strip())
        for j in list2:
            flist2.append(j.strip())
        if len(flist1) != len(flist2):
            return False
        else:
            x1 = set()
            y1 = set()
            x2 = set()
            y2 = set()
            for i in range(len(flist1)):
                pre1 = re.findall(r'(.*)\=',flist1[i],re.S)[0]
                cons1 = re.findall(r'\=(.*)',flist1[i],re.S)[0]
                pre2 = re.findall(r'(.*)\=',flist2[i],re.S)[0]
                cons2 = re.findall(r'\=(.*)',flist2[i],re.S)[0]
                x1.add(pre1)
                x2.add(pre2)
                y1.add(cons1)
                y2.add(cons2)
            if x1 == x2 and y1 == y2:
                return True
            else:
                return False

    def getFormulaLength(self,form):
        result = re.findall(r'~\((.*)\)',form,re.S)[0]
        list = result.split('&')
        return len(list)

    def getMaxLengthInList(self, flist):
        max = 0
        for f in flist:
            if max < self.getFormulaLength(f):
                max = self.getFormulaLength(f)
        return max

    def getSameLengthInList(self,flist,length):
        list = []
        for f in flist:
            if self.getFormulaLength(f)==length:
                list.append(f)
        return list

    def removeSamePatInList(self, flist):
        mlen = self.getMaxLengthInList(flist)
        totallist = []
        for i in range(mlen+1):
            if i ==0 or i ==1 :
                continue
            else:
                nlist = self.getSameLengthInList(flist,i)
                nonrlist = nlist
                for j in nlist:
                    for k in nlist[nlist.index(j)+1::]:
                        if self.judgeExistSameFormula(j,k):
                            nonrlist.remove(k)
                totallist.extend(nonrlist)
        return totallist

    def normalize(self,form):
        temp = re.findall(r'~\((.*)\)', form, re.S)[0]
        list = temp.split('&')
        count = 1
        tlist = []
        for i in list:
            tlist.append(i.strip())
        flist = []
        for t in tlist:
            if ' ' in t:
                temp = re.findall(r'(\w*\s\w*)=', t, re.S)[0]
                value = re.findall(r'=(.*)', t, re.S)[0]
                if count == 1:
                    temp = temp[:-1] + 'i' + '=' + value
                else:
                    temp = temp[:-1] + 'j' + '=' + value
                count += 1
                flist.append(temp)
            else:
                flist.append(t)
        str1 = '~(' + ' & '.join(flist) + ')'
        return str1

    def singleFormEqual(self, form1, form2):
        if ' ' in form1 and ' ' not in form2:
            return False
        elif ' ' in form2 and ' ' not in form1:
            return False
        else:
            if ' ' in form1:
                str1 = re.findall(r'(\w*)\s{1}(\w*)\=(\w*)', form1, re.S)[0]
                str2 = re.findall(r'(\w*)\s{1}(\w*)\=(\w*)', form2, re.S)[0]
                if str1[0] == str2[0] and str1[2] == str2[2]:
                    return True
                else:
                    return False
            else:
                str1 = re.findall(r'(\w*)\=(\w*)', form1, re.S)[0]
                str2 = re.findall(r'(\w*)\=(\w*)', form2, re.S)[0]
                if str1[0] == str2[0] and str1[1] == str2[1]:
                    return True
                else:
                    return False

    def mutleFormEqual(self, form1, form2):
        str1 = re.findall(r'\((.*?)\)', form1, re.S)[0]
        str2 = re.findall(r'\((.*?)\)', form2, re.S)[0]
        tlist1 = str1.split('&')
        list1 = []
        for t1 in tlist1:
            list1.append(t1.strip())
        tlist2 = str2.split('&')
        list2 = []
        for t2 in tlist2:
            list2.append(t2.strip())
        vlist1 = []
        vlist2 = []
        for f1 in list1:
            if ' ' in f1:
                value1 = re.findall(r'(\w*)\s{1}(\w*)\=(\w*)', f1, re.S)[0][2]
            else:
                value1 = re.findall(r'(\w*)\=(\w*)',f1,re.S)[0][1]
            vlist1.append(value1)
        for f2 in list2:
            if ' ' in f2:
                value2 = re.findall(r'(\w*)\s{1}(\w*)\=(\w*)', f2, re.S)[0][2]
            else:
                value2 = re.findall(r'(\w*)\=(\w*)',f2,re.S)[0][1]
            vlist2.append(value2)
        if len(list1) != len(list2):
            return False
        elif set(vlist1) != set(vlist2):
            return False
        else:
            for i in vlist1:
                if i not in vlist2:
                    return False
                else:
                    index1 = vlist1.index(i)
                    index2 = vlist2.index(i)
                    if not self.singleFormEqual(list1[index1],list2[index2]):
                        return False
        return True

    def ForminListEqu2Form(self, form, l):
        for f in l:
            if self.mutleFormEqual(f, form):
                return True
        return False

    def changeFormulaIntoSmv(self, form1):
        inner = re.findall(r'\((.*?)\)', form1, re.S)[0]
        innerlist = inner.split('&')
        smvlist = []
        for i in innerlist:
            before = re.findall(r'(.*)=', i.strip(), re.S)[0]
            after = re.findall(r'=(.*)', i.strip(), re.S)[0].replace('True', 'TRUE').replace('False', 'FALSE')
            if ' ' in before:
                var = re.findall(r'(.*)\s', before, re.S)[0]
                param = re.findall(r'\s(.*)', before, re.S)[0].replace('i','1').replace('j','2')
                newbefore = var+'['+param+']'
                smvlist.append('(' + newbefore +' = ' + after + ')')
            else:
                smvlist.append('(' + before + ' = ' + after + ')')
        str = ' & '.join(smvlist)
        return '(!('+str+'))'

    def judgeTrueOfForm(self, form):
        inner = re.findall(r'\((.*?)\)', form, re.S)[0]
        innerlist = inner.split('&')
        varDict = dict()
        for i in innerlist:
            before = re.findall(r'(.*)=', i.strip(), re.S)[0]
            after = re.findall(r'=(.*)', i.strip(), re.S)[0]
            if before not in varDict:
                varDict[before] = after
            else:
                if varDict[before] != after:
                    return True
        return False

    def formulaExistRelationInList(self, form, fl):
        for f in fl:
            if self.subFormula(form, f) != -1:
                return True
            elif self.mutleFormEqual(form,f):
                return True
        return False

    def constructGraph(self, formlist, invdict):
        array = np.eye(len(formlist))
        for f in formlist:
            for k, v in invdict.items():
                if self.formulaExistRelationInList(f, v):
                    array[formlist.index(k)][formlist.index(f)] = 1
        return array

    def judgeStrongConnect(self, array):
        n = len(array)
        a = mat(array)  # 转化为可计算的矩阵
        b = mat(zeros((n, n)))  # 设置累加矩阵
        for i in range(1, n + 1):  # 累加过程
            b += a ** n
        if 0 in b:  # 判断是不是强连通
            return False
        else:
            return True

    def subFormula(self, form1, form2):
        str1 = re.findall(r'\((.*?)\)', form1, re.S)[0]
        list1 = str1.split('&')
        tlist = []
        for l1 in list1:
            tlist.append(l1.strip())
        str2 = re.findall(r'\((.*?)\)', form2, re.S)[0]
        list2 = str2.split('&')
        tlist2 = []
        for l2 in list2:
            tlist2.append(l2.strip())
        if set(tlist) < set(tlist2):
            return 1
        elif len(tlist) < len(tlist2):
            templist = []
            for i in set(tlist):
                flag = False
                for j in set(tlist2):
                    if self.singleFormEqual(i, j):
                        templist.append(j)
                        flag = True
                if not flag:
                    return -1
            if set(tlist) > set(templist):
                return -1
            if flag:
                return 1
        elif set(tlist) == set(tlist2):
            return 0
        else:
            return -1


if __name__ == '__main__':
    p = load_system('n_mutual.json')
    str1 = '~(n j=try & n i=crit & x=True)'
    str2 = '~(n j=try & n i=crit)'
    str3 = '~(n j=try & x=True)'
    str4 = '~(n i=exit)'
    str5 = '~(n i=exit & n i=idle & x=False)'
    str6 = '~(n i=try & x=True & n j=idle)'
    str7 = '~(x=True & n j=crit)'
    str8 = '~(n i=crit & x=True)'
    fl = ['~(x=True & n j=crit)', '~(n i=exit & n j=crit)', '~(n i=crit & n j=crit)', '~(x=True & n i=exit)', '~(x=False & n j=exit & n i=exit)']
    d =  {'~(n i=crit & n j=crit)': ['~(x=True & n j=crit & n i=try)'], '~(x=True & n j=crit)': ['~(x=False & n j=crit & n i=exit)'], '~(n j=crit & n i=exit)': ['~(n j=crit & n i=crit)', '~(x=True & n i=exit & n j=try)'], '~(x=True & n i=exit)': ['~(x=True & n i=crit)', '~(x=False & n i=exit & n j=exit)'], '~(n i=exit & n j=exit)': ['~(n i=crit & n j=exit)']}

    l =  ['~(n i=crit & n j=crit)', '~(x=True & n j=crit)', '~(n j=crit & n i=exit)', '~(x=True & n i=exit)', '~(n i=exit & n j=exit)']
    print(p.formulaExistRelationInList('~(n i=crit & n j=crit)', ['~(x=True & n i=try & n j=crit)']))
    print(p.subFormula('~(n i=crit & n j=crit)', '~(x=True & n i=try & n j=crit)'))
    print(p.constructGraph(l, d))
    print(l)
    # print(p.mutleFormEqual('~(n i=crit & n j=exit)', '~(n i=exit & n j=crit)'))
    print(p.judgeStrongConnect(p.constructGraph(l, d)))
