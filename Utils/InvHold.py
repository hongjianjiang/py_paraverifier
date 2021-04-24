from type import *
from z3 import *
def weakprecondition(statement, formula):
    #judge the type of the given statement
    varsInformula = formula.getVars()
    if statement.isAssign():
        #single assign condition
        var = statement.getVar()
        exp = statement.getExp()
        if not var in varsInformula: #assignment has no affection on formula
            resultFormula = formula
        else:#has side effection

    else:
        #parall assignment condition
        vars = statement.getVars()
        exps = statement.getExps()
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

statement  = SAssign("n",EVar("C"))

statement1 = SAssign("x",FChaos())

formula = FChaos()

statement2 = SParallel([statement, statement1])
weakprecondition(statement2, formula)

