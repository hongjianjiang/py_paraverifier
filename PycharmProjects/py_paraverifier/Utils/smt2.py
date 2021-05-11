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

    def getStringInFormula(self,formula):
        result = re.findall(r'[(](.*)[)]', formula, re.S)
        return result[0]

    def getStringVarinFormula(self,formula):
        result = re.findall(r'[\[](.*)[\]]', formula, re.S)
        return result[0]

    def getPrefixInArray(self,formula):
        if '[' in formula:
            result = re.findall(r"(.*?)\[.*\]+", formula, re.S)
            res = result[0]
        else:
            res= formula
        return res

    def getEqualFirst(self,formula):
        result = re.findall(r'.+?(?==)',formula,re.S)
        return result[0]

    def getEqualSecond(self,formula):
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
            str_formula += 'and'
            if '[' in nsf:
                str_context += ' (declare-const i Int) (declare-const j Int)'
            for i in (nsf.replace(' ', '').split('&')):
                l1 = i.split('=')
                str_formula +=' (='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif j in boollist:
                        str_formula += " " + j.lower()
                    elif self.getPrefixInArray(j) in vars:
                        if j.count('[') > 0:
                            vars1 = self.getStringVarinFormula(j)
                            str_formula += " (select "+self.getPrefixInArray(j) + " " + vars1 +')'
                        else:
                            str_formula += " "+j
                str_formula += ')'
            str_formula += '))'
        else:
            if '[' in nsf:
                str_context += ' (declare-const i Int)'
            for i in (nsf.replace(' ', '').split('&')):
                print(i)
                l1 = i.split('=')
                str_formula += '='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif j in boollist:
                        str_formula += " " + j.lower()
                    elif self.getPrefixInArray(j) in vars:
                        if j.count('[') > 0:
                            str_formula += " (select " + self.getPrefixInArray(j) + ' i)'
                        else:
                            str_formula += " " + j
                str_formula += ')'
            str_formula += ')'
        # print(str_context+str_formula)
        s.from_string(str_context+str_formula)
        if str(s.check())=="sat":
            print(s.model())

        return str(s.check())


if __name__ == '__main__':
    smt2 = SMT2('../Protocol/n_mutualEx.json')
    print(smt2.check("~(x=True & T=C)"))
    # print(smt2.check('~(n[i]=C & n[j]=C)'))
    #
    # s= Solver()
    # s.from_string("(declare-datatypes () ((state I T C E))) (declare-const n (Array Int state)) (declare-const x Bool) (declare-const i Int) (declare-const j Int) (assert (and (= (select n i ) C) (= (select n j) C) (not (= i j)) ))")
    # print(s.check())
    # print(s.model())
    # print(smt2.check("~(n[i]=T & x=True & C=C & n[j]=C)"))
    # print(smt2.check("~(x=True & n[j]=T)"))