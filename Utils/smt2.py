# coding=utf-8
#author: Hongjian Jiang

import json
import re
from z3 import Solver, parse_smt2_string

SPLIT_CHAR = ','


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

    def getPrefixInArray(self,formula):
        result = re.findall(r'(.*?)\[',formula,re.S)
        return result[0].replace('[','')

    def check(self, smt2_formula):
        s = Solver()
        nsf = self.getStringInFormula(smt2_formula)# the negation of the smt2 formula
        with open(self.file) as f:
            data = json.load(f)
            states = data['states']
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
                str_context += ' (declare-const i Int)'
            for i in (nsf.replace(' ', '').split('&')):
                l1 = i.split('=')
                str_formula +=' (='
                for j in l1:
                    if j in states:
                        str_formula += " "+j
                    elif self.getPrefixInArray(j) in vars:
                        if j.count('[') > 0:
                            str_formula += " (select "+self.getPrefixInArray(j) + ' i)'
                str_formula+=')'
            str_formula+= '))'
        else:
            if '[' in nsf:
                str_context += ' (declare-const i Int)'
            for i in (nsf.replace(' ', '').split('&')):
                l1 = i.split('=')
                str_formula += '='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif self.getPrefixInArray(j) in vars:
                        if j.count('[') > 0:
                            str_formula += " (select " + self.getPrefixInArray(j) + ' i)'
                str_formula += ')'
            str_formula += ')'
        s.from_string(str_context+str_formula)
        # s.add(parse_smt2_string((context if context else self.context) + smt2_formula))
        # print("--------------\n")
        # if str(s.check()) == "sat":
        #     print(s.model())
        # print("--------------\n")
        return str(s.check())


if __name__ == '__main__':
    smt2 = SMT2('../Protocol/n_mutualEx.json')
    # print(smt2.check("!(n[2]=C)"))
    print(smt2.check('!(T=C & n[2]=C)'))