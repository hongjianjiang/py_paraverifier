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

i1 = Intc(1)
print("test1:",i1)


class Strc(Const):
    '''
    type str
    '''
    def __init__(self, context):
        self.ty = Const.STRC
        self.context = context

    def __str__(self):
        return self.context


print("test2",Strc("abc"))
class Boolc(Const):
    '''
    type bool
    '''
    def __init__(self, context):
        self.ty = Const.BOOLC
        self.context = context

    def __str__(self):
        return self.context
print("test3:",Boolc("True"))

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

print("test4:",Paramdef("i","State"))
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
        return self.vars

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
        self.vars = [var]

    def __str__(self):
        return self.var


class EParamr(Exp):
    '''
    expression params
    '''
    def __init__(self,paramr):
        self.ty = Exp.PARAM
        self.paramr = paramr
        self.vars = []

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

class EUIF(Exp):
    '''
    express uif
    '''
    def __init__(self,name,*args):
        self.ty = Exp.UIF
        self.name = name
        self.explist = args
        self.vars = []

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


# f1 = FEqn(EVar("n1"), FMiracle())
# print(f1)

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
        return "!(%s)" % self.formula
# f1 = FEqn(EVar("n1"), FMiracle())
# fneg=FNeg(f1)
# print(fneg)
# fneg = FNeg(FMiracle())
# print(fneg)


class FAndlist(Formula):
    '''
    formula andlist
    '''
    def __init__(self,*args):
        self.ty = Formula.ANDLIST
        self.formulalist = args
        self.vars = [f.getVars() for f in self.formulalist[0]]
        self.exps = [f.getExps() for f in self.formulalist[0]]

    def getSubFormula(self):
        return self.formulalist[0]

    def getArgs(self):
        return self.formulalsit[0]

    def __str__(self):
        return "(" + " & ".join(self.formulalsit[0]) + ")"


class FOrlist(Formula):
    '''
    formula orlist
    '''
    def __init__(self, *args):
        self.ty = Formula.ORLIST
        self.formulalist = args
        self.vars = [f.getVars() for f in self.formulalist[0]]
        self.exps = [f.getExps() for f in self.formulalist[0]]

    def __str__(self):
        return "(" + " | ".join(self.formulalist[0]) + ")"


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


class ExistFormula(Formula):
    '''formula existformula'''
    def __init__(self,formula,*args):
        self.ty = Formula.EXISTFORMULA
        self.paradeflist = args
        self.formula = formula 
        self.vars = self.formula.getVars()
        self.exps = self.formula.getExps()


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
            self.vars.append(v.getVar())
        return self.vars

    def getExps(self):
        for v in self.statementlist[0]:
            self.exps.append(v.getExp())
        return self.exps


class Rule():
    '''
    rule definition
    '''
    def __init__(self,name,formula,statement,*args):
        self.name = name
        self.formula = formula 
        self.statement = statement
        self.params = args

    def __str__(self):
        return "rule:{\nname: " + str(self.name) + "\nparams: " + "".join([str(i) for i in self.params]) +"\nguard: " + str(self.formula) + "\naction"+ str(self.statement)+"\n}"


param = Paramdef("1", "client")
formula = FEqn(EVar("n1"),EVar("n2"))
# formula1 = FAndlist([FEqn(EVar("n1"),EConst("1")),FEqn(EVar("n2"),ECosnt("C"))])
e1 = EVar("v1")
e2 = EVar("v2")
formula1 = FEqn(e1,EConst("C"))
# print(formula1.getExps())
formula2 = FEqn(e2,EConst("C"))
formula3 = FAndlist([formula1,formula2])
print(formula3.getSubFormula())
# print(formula3.getVars())
# print(formula3.getExps())
# print(formula1.getExps())
statement = SAssign("n",EVar("C"))
r = Rule("try",formula,statement,param)


class Prop():
    '''
    definition property
    '''
    def __init__(self,name,formula,*args):
        self.name = name 
        self.formula = formula
        self.params = args

    def __str__(self):
        return "prop:{\nname: " + self.name + "\nparams:"+"".join([str(i) for i in self.params])  +"\ninv:" + str(self.formula)+"\n}"


prop = Prop("inv1",formula,param)
# print(prop)