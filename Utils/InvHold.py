#author: Hongjian Jiang


from gym.utils.type import *
from gym.utils.smt2 import *
from gym.utils.type import Var
import re


def weakestprecondition(statement, formula):
    '''
    :param statement: assignment or parallel assigement
    :param formula: given invariant formula
    :return: the string of the weakest precondtion
    '''
    # print('f:', formula, 's:', statement)
    varsInformula = formula.getVars()
    if '(' in str(formula):
        innform = re.findall(r'\((.*?)\)', str(formula), re.S)[0]
    else:
        innform = re.findall(r'~(.*)', str(formula), re.S)[0]
    varlist = []
    valuelist = []
    templist = innform.split('&')
    for i in templist:
        str1 = re.findall(r'(.*?)=', i, re.S)[0]
        str2 = re.findall(r'=(.*)', i, re.S)[0]
        varlist.append(str1.strip())
        valuelist.append(str2.strip())
    if statement.isAssign():        #single assign condition
        # print(statement,formula)
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
            if v in varlist:
                varlist[varlist.index(v)] = exps[i]
                resultFormula = resultFormula.replace(v,exps[i])
            else:
                pass
        resultFormula = '~('
        for i in range(len(varlist)):
            if i != len(varlist)-1:
                resultFormula += varlist[i]+ '='+valuelist[i] +' & '
            else:
                resultFormula += varlist[i]+ '='+valuelist[i]
        resultFormula+=')'
    # print('test:', 'statement:',statement, 'formula:',formula, 'result:', resultFormula)
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
    statement = SAssign(EVar(Var("n"),'j'),EConst(Var("exit")))
    statement1 = SAssign(EConst(Strc("x")),FChaos())
    formula = FNeg(FAndlist([FEqn(EVar(Var("n"),'i'),EConst(Strc("exit"))),FEqn(EVar(Var("n"),'j'),EConst(Strc("exit"))),FEqn(EConst(Strc("x")),EConst(Boolc("False")))]))
    statement2 = SParallel([statement, statement1])
    wp = weakestprecondition(statement2,formula)
    # print(invHoldForCondition3(FEqn(EVar(Var("n"),"j"),EConst(Strc("E")))),wp)