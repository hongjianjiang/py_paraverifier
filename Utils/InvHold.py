#author: Hongjian Jiang
from type import *
from z3 import *

def weakprecondition(statement, formula):
    '''
    :param statement: assignment or parallel assigement
    :param formula: given invariant formula
    :return: the string of the weakest precondtion
    '''
    #judge the type of the given statement
    resultFormula = FChaos()
    varsInformula = formula.getVars()
    if statement.isAssign():
        #single assign condition
        var = statement.getVar()
        exp = statement.getExp()
        if not str(var) in varsInformula: #assignment has no affection on formula
            resultFormula = str(formula)
        else:#has side effection
            resultFormula = (str(formula).replace(str(var),str(exp)))
    else:
        #parall assignment condition
        vars = statement.getVars()
        exps = statement.getExps()
        for i,v in enumerate(vars):
            if v in varsInformula:
                resultFormula= (str(formula).replace(v,exps[i]))
    return resultFormula


def invHoldCondition(statement, formula):
    wp = weakprecondition(statement,formula)
    solver = Solver()
    solver.add(wp)
    solver.check()
    if solver.check() == sat:
        flag = 1
    elif wp == formula:
        flag = 2
    else:
        flag = 3
    return flag

print("====================")
statement = SAssign(Var("n",[1]),EVar("C"))
statement1 = SAssign("x",FChaos())
formula = FNeg(FAndlist([FEqn(EVar(Var("n",[1])),EConst(Strc("C"))),FEqn(EVar(Var("n",[2])),EConst(Strc("C")))]))
statement2 = SParallel([statement, statement1])
print(weakprecondition(statement2, formula))
invHoldCondition(statement2,formula)

