#author: Hongjian Jiang


from type import *
from smt2 import *
import re


def weakestprecondition(statement, formula):
    '''
    :param statement: assignment or parallel assigement
    :param formula: given invariant formula
    :return: the string of the weakest precondtion
    '''
    varsInformula = formula.getVars()
    if statement.isAssign():        #single assign condition
        var = statement.getVar()
        exp = statement.getExp()
        if not str(var) in varsInformula: #assignment has no affection on formula
            resultFormula = str(formula)
        else:#has side effection
            resultFormula = (str(formula).replace(str(var),str(exp)))
    else:        #parall assignment condition
        vars = statement.getVars()
        exps = statement.getExps()
        resultFormula = str(formula)
        for i,v in enumerate(vars):
            if v in varsInformula:
                resultFormula = resultFormula.replace(v,exps[i])
            else:
                pass
    return resultFormula


def invHoldCondition(statement, formula, file):
    '''
    :param statement: the statement of the guarded command
    :param formula: the invariant formula
    :return: the condition of which invhold meets
    '''
    smt2 = SMT2(file)
    wp = weakestprecondition(statement,formula)
    # print("assign:", statement,"\ninv:", formula)
    # print(wp,statement,formula)
    if smt2.check(wp) == "unsat":
        flag = 1
    elif str(wp) == str(formula):
        flag = 2
    else:
        flag = 3
    return flag


def invHoldForCondition3(guard, formula):
    '''
    :param guard: the formula of the guard command
    :param formula: the formula of the weakest precondition
    :return: the disconjunction of the guard and the formula
    '''
    negg = FNeg(guard)
    if '(' not in str(formula):
        strform = '('+str(formula).replace('~','')+')'
    else:
        strform = str(formula)
    if '(' in str(guard):
        guard_str=re.findall(r'[(](.*)[)]', str(negg), re.S)
    else:
        guard_str=[str(guard)]
    formula_str=re.findall(r'[(](.*)[)]', strform, re.S)
    guard_str.append(formula_str[0])
    result = " & ".join(guard_str)
    return "~("+result+")"


if __name__ == '__main__':
    statement = SAssign(EVar(Var("n"),'j'),EConst(Var("I")))
    statement1 = SAssign(EConst(Strc("x")),FChaos())
    formula = FNeg(FAndlist([FEqn(EVar(Var("n"),'i'),EConst(Strc("C"))),FEqn(EConst(Strc("x")),EConst(Boolc("True")))]))
    statement2 = SParallel([statement, statement1])
    wp = weakestprecondition(statement2,formula)
    # print(invHoldForCondition3(FEqn(EVar(Var("n"),"j"),EConst(Strc("E")))),wp)