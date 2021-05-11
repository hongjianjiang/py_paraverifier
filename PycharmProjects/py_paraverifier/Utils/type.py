#author: Hongjian Jiang
class Const():
    '''
    Type Const:int, str, bool
    '''
    INTC, STRC, BOOLC = range(3)

    def __init__(self):
        pass

    def isIntc(self):
        return self.ty == self.INTC

    def isBoolc(self):
        return self.ty == self.BOOLC

    def isStrc(self):
        return self.ty == self.STRC

    def getContext(self):
        return self.context


class Intc(Const):
    '''
    type int
    '''
    def __init__(self, context):
        self.ty = Const.INTC
        self.context = context

    def __str__(self):
        return str(self.context)


class Strc(Const):
    '''
    type str
    '''
    def __init__(self, context):
        self.ty = Const.STRC
        self.context = context

    def __str__(self):
        return self.context


class Boolc(Const):
    '''
    type bool
    '''
    def __init__(self, context):
        self.ty = Const.BOOLC
        self.context = context

    def __str__(self):
        return self.context


class Typedef():
    '''
    type def
    '''
    def __init__(self, name, *args):
        self.name = name
        self.range = args


class Paramdef():
    '''
    params definition
    '''
    def __init__(self, name, typename):
        self.name = name
        self.typename = typename

    def __str__(self):
        return self.typename + "[" + self.name + "]"


class Paramr():
    '''
    params reference
    '''
    PARAMREF,PARAMFIX = range(2)

    def __init__(self):
        pass

    def isParamref(self):
        return self.ty == self.PARAMREF

    def isParamfix(self):
        return self.ty == self.PARAMFIX


class Paramref(Paramr):
    def __init__(self,name):
        self.name = name
        self.ty = Paramr.PARAMREF

    def __str__(self):
        return self.name

class Paramfix(Paramr):
    def __init__(self, vn, tn, value):
        self.ty = Paramr.PARAMFIX
        self.varname = vn
        self.typename = tn
        self.value = value


class Vardef():
    '''
    variables definition
    '''
    def __init__(self,arrname,*args,typename):
        self.typename= typename
        self.arrname = arrname,
        self.params=args


class Var():
    def __init__(self, name, *args):
        self.name = name 
        self.indexs = args

    def __str__(self):
        str1 = ""
        if len(self.indexs[0]) > 0:
            for i in self.indexs[0]:
                str1+=self.name+"["+str(i)+"]"
        else:
            str1 = self.name
        return str1


class Exp():
    '''
    type expression: const, var, params, ite, uif
    '''
    CONST, VAR, PARAM, ITE, UIF = range(5)

    def __init__(self):
        pass

    def isConst(self):
        return self.ty == self.CONST

    def isVar(self):
        return self.ty == self.VAR

    def isParam(self):
        return self.ty == self.PARAM

    def isIte(self):
        return self.ty == self.ITE

    def isUif(self):
        return self.ty == self.UIF

    def getVars(self):
        return self.vars


class Formula():
    '''
    type formula: chaos(T), miracle(F), uip, eqn, neg, andlist, orlist, imply, forallformula, existformula
    '''
    CHAOS, MIRACLE, UIP, EQN, NEG, ANDLIST, ORLIST, IMPLY, FORALLFORMULA, EXISTFORMULA = range(10)

    def __init__(self):
        pass

    def isChaos(self):
        return self.ty == self.CHAOS

    def isMiracle(self):
        return self.ty == self.MIRACLE

    def isUip(self):
        return self.ty == self.UIP

    def isEqn(self):
        return self.ty == self.EQN

    def isNeg(self):
        return self.ty == self.NEG

    def isAndList(self):
        return self.ty == self.ANDLIST

    def isOrList(self):
        return self.ty == self.ORLIST

    def isImply(self):
        return self.ty == self.IMPLY

    def isForAllFormula(self):
        return self.ty == self.FORALLFORMULA

    def isExistFormula(self):
        return self.ty == self.EXISTFORMULA

    def getVars(self):
        return [str(v) for v in self.vars]

    def getExps(self):
        return self.exps

    def getSubFormula(self):
        pass



class EConst(Exp):
    '''
    Expression of Const
    '''
    def __init__(self,context):
        self.ty = Exp.CONST
        self.context = context
        self.vars = []

    def __str__(self):
        return str(self.context)


class EVar(Exp):
    '''
    Expression of Var
    '''
    def __init__(self, var):
        self.ty = Exp.VAR
        self.var = var 
        self.vars = [str(var)]

    def __str__(self):
        return str(self.var)


class EParamr(Exp):
    '''
    expression params
    '''
    def __init__(self,paramr):
        self.ty = Exp.PARAM
        self.paramr = paramr
        self.vars = []

    def __str__(self):
        return str(self.paramr)


class FChaos(Formula):
    '''
    formula Chaos
    '''
    def __init__(self):
        self.ty = Formula.CHAOS
        self.vars = []
        self.exps = ["T"]

    def __str__(self):
        return "True"


class FMiracle(Formula):
    '''
    formula Miracle
    '''
    def __init__(self):
        self.ty = Formula.MIRACLE
        self.vars = []
        self.exps = ["T"]

    def __str__(self):
        return "False"


class EIte(Exp,Formula):
    '''
    expresss ite
    '''
    def __init__(self,form,exp1,exp2):
        self.ty = Exp.ITE
        self.form = form
        self.exp1 = exp1 
        self.exp2 = exp2 
        self.vars = self.exp1.getVars() + self.exp2.getVars()

    def __str__(self):
        return "If " + str(self.form) +" then " + str(self.exp1) + " else "+ str(self.exp2)


class EUIF(Exp):
    '''
    express uif
    '''
    def __init__(self,name,*args):
        self.ty = Exp.UIF
        self.name = name
        self.explist = args
        self.vars = []


class FUip(Formula):
    '''
    formula uip
    '''
    def __init__(self, name, *args):
        self.ty = Formula.UIP
        self.name = name 
        self.explist = args
        self.vars = [e.getVars() for e in self.explist]
        self.exps = [e.getExps() for e in self.explist]


class FEqn(Formula):
    '''
    formula eqn
    '''
    def __init__(self, e1, e2):
        self.ty = Formula.EQN
        self.exp1 = e1
        self.exp2 = e2
        self.vars = self.exp1.getVars() + self.exp2.getVars()
        self.exps = [self.exp1] + [self.exp2]

    def __str__(self):
        return str(self.exp1) + "=" + str(self.exp2)


class FNeg(Formula):
    '''
    formula neg
    '''
    def __init__(self,f):
        self.ty = Formula.NEG
        self.formula = f 
        self.vars = self.formula.getVars()
        self.exps = self.formula.getExps()

    def __str__(self):
        return "~%s" % self.formula


class FAndlist(Formula):
    '''
    formula andlist
    '''
    def __init__(self,*args):
        self.ty = Formula.ANDLIST
        self.formulalist = args
        self.vars = []
        self.exps = [f.getExps() for f in self.formulalist[0]]

    def getSubFormula(self):
        return [str(f) for f in self.formulalist[0]]

    def getArgs(self):
        return self.formulalist[0]

    def getVars(self):
        for f in self.formulalist[0]:
            self.vars +=f.getVars()
        return self.vars

    def __str__(self):
        return "(" + " & ".join([str(f) for f in self.formulalist[0]]) + ")"


class FOrlist(Formula):
    '''
    formula orlist
    '''
    def __init__(self, *args):
        self.ty = Formula.ORLIST
        self.formulalist = args
        self.vars = []
        self.exps = [f.getExps() for f in self.formulalist[0]]

    def __str__(self):
        return "(" + " | ".join([str(f) for f in self.formulalist[0]]) + ")"

    def getSubFormula(self):
        return [str(f) for f in self.formulalist[0]]

    def getVars(self):
        for f in self.formulalist[0]:
            self.vars +=f.getVars()
        return self.vars



class FImply(Formula):
    '''formula imply'''
    def __init__(self, f1, f2):
        self.ty = Formula.IMPLY
        self.formula1 = f1 
        self.formula2 = f2 
        self.vars = self.formula1.getVars() + self.formula2.getVars()
        self.exps = self.formula1.getExps() + self.formula2.getExps()

    def __str__(self):
        return str(self.formula1) + " -> " + str(self.formula2)

    def getSubFormula(self):
        return [str(self.formula1),str(self.formula2)]

    # def getVars(self):
    #     for f in self.formula2.getVars():
    #         print(f)
    #         self.formula1.getVars().append(f)
    #     print(self.formula1.getVars())
    #     return self.formula1.getVars()


class ForallFormula(Formula):
    '''
    formula forallformula
    '''
    def __init__(self, formula, *args):
        self.ty = Formula.FORALLFORMULA
        self.paradeflist = args
        self.formula = formula 
        self.vars = self.formula.getVars()
        self.exps = self.formula.getExps()

    def __str__(self):
        return "forall "+ ",".join([str(p) for p in self.paradeflist[0]])+ " in " + str(self.formula)


class ExistFormula(Formula):
    '''formula existformula'''
    def __init__(self,formula,*args):
        self.ty = Formula.EXISTFORMULA
        self.paradeflist = args
        self.formula = formula 
        self.vars = self.formula.getVars()
        self.exps = self.formula.getExps()

    def __str__(self):
        return "exist "+ ",".join([str(p) for p in self.paradeflist[0]])+ " in " + str(self.formula)


class Statement():
    '''
    statement type
    '''
    ASSIGN,PARALLEL= range(2)

    def __init__(self):
        pass

    def isAssign(self):
        return self.ty == self.ASSIGN

    def isParallel(self):
        return self.ty == self.PARALLEL


class SAssign(Statement):
    '''
    statement assign
    '''
    def __init__(self,var,exp):
        self.ty = Statement.ASSIGN
        self.var = var  
        self.exp = exp

    def __str__(self):
        return str(self.var) + " := " + str(self.exp)

    def getVar(self):
        return self.var

    def getExp(self):
        return self.exp


class SParallel(Statement):
    '''
    statement parallel
    '''
    def __init__(self,*args):
        self.ty = Statement.PARALLEL
        self.statementlist = args
        self.vars = []
        self.exps = []

    def __str__(self):
        return " ; ".join([ str(v) for v in self.statementlist[0]])

    def getVars(self):
        for v in self.statementlist[0]:
            self.vars.append(str(v.getVar()))
        return self.vars

    def getExps(self):
        for v in self.statementlist[0]:
            self.exps.append(str(v.getExp()))
        return self.exps


class Rule():
    '''
    rule definition
    '''
    def __init__(self,formula,statement,*args):
        # self.name = name
        self.formula = formula 
        self.statement = statement
        self.params = args

    def __str__(self):
        return "rule " +"".join([str(i) for i in self.params]) +"\nguard: " + str(self.formula) + "\naction: "+ str(self.statement)+"\n}"

    def getStatement(self):
        return self.statement

    def getGuard(self):
        return self.formula

    def getArgs(self):
        return self.params


class Prop():
    '''
    definition property
    '''
    def __init__(self,formula,*args):
        # self.name = name
        self.formula = formula
        self.params = args

    def __str__(self):
        # return "prop:{\nname: " + self.name + "\nparams:"+"".join([str(i) for i in self.params])  +"\ninv:" + str(self.formula)+"\n}"
        return "prop:{params:"+"".join([str(i) for i in self.params])  +"\ninv:" + str(self.formula)+"\n}"

    def getInv(self):
        return self.formula

    def getArgs(self):
        return self.params

if __name__ == '__main__':
    print("test1:",Intc(1))
    print("test2",Strc("abc"))
    print("test3:",Boolc("True"))
    print("test4:",Paramdef("i","State"))
    print("test5:",Var("n",[1]))
    print("test6:", EConst(Boolc("True")))
    print(EConst(Boolc("True")).getVars())
    print("test7:",EVar(Var("n",[1,2,3,4])))
    print(EVar(Var("n",[1])).getVars())
    print("test8:",EParamr(Paramdef("i","State")))
    print("test9:",FChaos())
    print("test10:",FMiracle())
    print("test11:",EIte(FMiracle(),EVar(Var("n",[1,2,3,4])),EVar(Var("n",[1,2,3,4]))))
    print(EIte(FMiracle(),EVar(Var("n",[1])),EVar(Var("n",[1,2,3,4]))).getVars())
    print("test12:",FEqn(EVar(Var("Name",[])),EConst(Strc("I"))))
    print(FEqn(EVar(Var("N",[1])),EConst(Strc("I"))).getVars())
    print(EVar(Var("N",[1])).getVars())
    print(EVar(Var("N",[1])).getVars() == FEqn(EVar(Var("N",[1])),EConst(Strc("I"))).getVars())
    print("test13:",FNeg(FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))))
    print(FNeg(FEqn(EVar(Var("N",[1])),EConst(Strc("I")))).getVars())
    print("test14:", FAndlist([FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))]))
    print(FAndlist([FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))]).getSubFormula())
    print( FAndlist([FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))]).getVars())
    print("test15:",FOrlist([FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))]))
    print(FOrlist([FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))]).getSubFormula())
    print(FOrlist([FEqn(EVar(Var("Name",[])),EConst(Strc("I"))),FEqn(EVar(Var("Name",[])),EConst(Strc("T")))]).getVars())
    print("test16:", FImply(FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),FEqn(EVar(Var("Name",[])),EVar(Var("Age",[])))))
    print(FImply(FEqn(EVar(Var("Name",[])),EConst(Strc("I"))),FEqn(EVar(Var("Name1",[])),EVar(Var("Mae1",[])))).getVars())
    print("test17:",ForallFormula(FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),[Paramdef("i","State"),Paramdef("j","State")]))
    print(ForallFormula(FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),[Paramdef("i","State"),Paramdef("j","State")]).getVars())
    print("test18:",ExistFormula(FEqn(EVar(Var("Name",[])),EVar(Var("Age",[]))),[Paramdef("i","State")]))
    print("test19:",SAssign(Var("n",[1]),EConst(Strc("I"))))
    print(SAssign(Var("n",[1]),EConst(Strc("T"))).getExp())
    print("test20: ",SParallel([SAssign(Var("n",[1]),EConst(Boolc("True"))),SAssign(Var("x",[]),EConst(Boolc("True")))]))
    print(SParallel([SAssign(Var("n",[1]),EConst(Boolc("True"))),SAssign(Var("x",[]),EConst(Boolc("True")))]).getExps())
    print("test21:", Rule("try", FEqn(EVar("n"), EConst(Strc("I"))), SAssign("n", EVar("T")), Paramdef("1", "client")))
    prop = Prop("mutualEx", FNeg(FAndlist([FEqn(EVar(Var("n", [1])), EConst(Strc("C"))), FEqn(EVar(Var("n", [1])), EConst(Strc("C")))])), [1, 2])
    # print("test22:",prop.getArgs())
