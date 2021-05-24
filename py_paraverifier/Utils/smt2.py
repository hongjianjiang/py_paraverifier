# coding=utf-8
#author: Hongjian Jiang

import json
import re
from z3 import Solver


class SMT2(object):
    '''
    Given the protocol's json file address and the invariant
    Json file servers as the context of the z3 environment
    Invariant servers as the assertation
    SMT2 returns the bool value whether it is true or not
    '''
    def __init__(self, file):
        super(SMT2, self).__init__()
        self.file = file

    def getStringInFormula(self, formula):
        '''
        :param formula: ~( a = b & b=c )
        :return: a = b & b = c
        '''
        result = re.findall(r'[(](.*)[)]', formula, re.S)
        return result[0]

    # def getStringVarinFormula(self,formula):
    #     result = re.findall(r'[\[](.*)[\]]', formula, re.S)
    #     return result[0]

    def getStringVarinFormula(self, formula):
        '''
        :param formula: n i = C & n j = C
        :return: [i,j]
        '''
        result = re.findall(r'\w*\s{1}(\w*)\s*', formula, re.S)
        return result

    def getPrefixInArray(self, formula):
        if " " in formula:
            result = re.findall(r'(\w*)\s{1}\w*\s*', formula, re.S)
            return result
        else:
            return formula

    def getEqualFirst(self, formula):
        result = re.findall(r'.+?(?==)', formula, re.S)
        return result[0]

    def getEqualSecond(self, formula):
        result = re.findall(r'(?<==).+', formula, re.S)
        return result[0]

    def check(self, smt2_formula):
        s = Solver()
        nsf = self.getStringInFormula(smt2_formula).replace("(","").replace(")","") # the negation of the smt2 formula
        with open(self.file) as f:
            data = json.load(f)
            states = data['states']
            boollist = ["True","False"]
            vars = data['vars']
            str_tmp = ""
            str_tmp1 = ""
            for i in states:
                str_tmp += " "+ i
            str_states = '(declare-datatypes () ((state' + str_tmp + ')))'
            for i in vars:
                if '=>' in vars[i]:
                    str_tmp1 += ' (declare-const '+ i +' (Array Int state))'
                elif 'bool' in vars[i]:
                    str_tmp1 += ' (declare-const '+ i + ' Bool)'
            str_context = str_states + str_tmp1
        str_formula = " (assert ("
        if '&' in nsf:
            ids = []
            str_formula += 'and'
            for i in (nsf.split('&')):
                l1 = i.strip().split('=')
                for id in l1:
                    if len(self.getStringVarinFormula(id)) > 0:
                        for i in self.getStringVarinFormula(id):
                            if i not in ids:
                                str_context += ' (declare-const %s Int)' % i
                                ids.append(i)
                str_formula +=' (='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif j in boollist:
                        str_formula += " " + j.lower()
                    elif self.getPrefixInArray(j)[0] in vars:
                        if j.count(' ') > 0:
                            vars1 = self.getStringVarinFormula(j)[0]
                            str_formula += " (select "+self.getPrefixInArray(j)[0] + " " + vars1 +')'
                        else:
                            str_formula += " "+j
                str_formula += ')'
            str_formula += '))'
        else:
            if len(self.getStringVarinFormula(nsf)) > 0:
                str_context += ' (declare-const %s Int)' % (self.getStringVarinFormula(nsf)[0])
            for i in (nsf.split('&')):
                l1 = i.split('=')
                str_formula += '='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif j in boollist:
                        str_formula += " " + j.lower()
                    elif self.getPrefixInArray(j)[0] in vars:
                        if j.count(' ') > 0:
                            str_formula += " (select " + self.getPrefixInArray(j)[0] + ' i)'
                        else:
                            str_formula += " " + j
                str_formula += ')'
            str_formula += ')'
        # print(str_formula)
        # print(str_context+str_formula)
        s.from_string(str_context+str_formula)
        # if str(s.check()) == "sat":
        #     print(s.model())

        return str(s.check())


if __name__ == '__main__':
    smt2 = SMT2('../Protocol/n_mutual.json')
    # print(smt2.check("~(x=True & n j=T)"))
    print(smt2.check('~(n i =C)'))
    # s= Solver()
    # s.from_string("(declare-datatypes () ((state I T C E))) (declare-const n (Array Int state)) (declare-const x Bool) (declare-const i Int) (declare-const j Int) (assert (and (= (select n i ) C) (= (select n j) C) (not (= i j)) ))")
    # print(s.check())
    # print(s.model())
    # print(smt2.check("~(n[i]=T & x=True & C=C & n[j]=C)"))
    # print(smt2.check("~(x=True & n[j]=T)"))