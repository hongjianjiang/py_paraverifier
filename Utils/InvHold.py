#author: Hongjian Jiang


from Utils.type import *
from Utils.smt2 import *
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
        print("invHold for case 1")
        flag = 1
    elif str(wp) == str(formula):
        print("invHold for case 2")
        flag = 2
    else:
        print("invHold for case 3")
        flag = 3
    print('====================================')
    return flag


def invHoldForCondition3(guard, formula):
    '''
    :param guard: the formula of the guard command
    :param formula: the formula of the weakest precondition
    :return: the disconjunction of the guard and the formula
    '''
    negg = FNeg(guard)
    guard_str=re.findall(r'[(](.*)[)]', str(negg), re.S)
    formula_str=re.findall(r'[(](.*)[)]', str(formula), re.S)
    guard_str.append(formula_str[0])
    result = " & ".join(guard_str)
    return "~("+result+")"


if __name__ == '__main__':
    statement = SAssign(EVar(Var("n"),'i'),EConst(Var("T")))
    # print(statement.isAssign())
    # statement1 = SAssign("x",FChaos())
    formula = FNeg(FAndlist([FEqn(EVar(Var("n"),'i'),EConst(Strc("C"))),FEqn(EVar(Var("n"),'j'),EConst(Strc("C")))]))
    # statement2 = SParallel([statement, statement1])
    # print(statement2.isAssign())
    wp = weakestprecondition(statement,formula)
    # guard = FAndlist([FEqn(EVar(Var("n",['i'])),EConst(Strc("T"))),FEqn(EVar(Var("x",[])),EConst(Boolc("True")))])
    # print(guard)
    # print(statement2)
    print(wp)
    # try_assign = SAssign(Var("n",['i']),EVar("T"))
    # wp1 = weakestprecondition(try_assign,formula)
    # print(wp1)
    # invHoldCondition(statement, formula,'../Protocol/n_mutualEx.json')
    # print(invHoldForCondition3(guard,wp))