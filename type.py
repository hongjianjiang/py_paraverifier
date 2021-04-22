
class Const():
    INTC,STRC,BOOLC = range(3)
    def __init__(self):
        pass
    def isIntc(self):
        return self.ty == INTC


class Intc(Const):
    def __init__(self,context):
        self.ty = Const.INTC
        self.context = context

class Strc(Const):
    def __init__(self,context):
        self.ty = Const.STRC
        self.context = context

class Boolc(Const):
    def __init__(self,context):
        self.ty = Const.BOOLC
        self.context = context

class Typedef():
    def __init__(self,name,*args):
        self.name = name
        self.range = args


class Paramdef():
    def __init__(self,name,typename):
        self.name = name
        self.typename = typename

class Paramr():
    PARAMREF,PARAMFIX = range(2)
    def __init__(self):
        pass

class Paramref(Paramr):
    def __init__(self,name):
        self.name = name
        self.ty = Paramr.PARAMREF

class Paramfix(Paramr):
    def __init__(self,vn,tn,value):
        self.ty = Paramr.PARAMFIX
        self.varname = vn
        self.typename = tn
        self.value = const

class Vardef():
    #params's element is paramdef type
    def __init__(self,arrname,*args,typename):
        self.typename= typename
        self.arrname  = arrname,
        self.params=args

class Var():
    def __init__(self,name,*args):
        self.name = name 
        self.indexs = args

class Exp():
    CONST,VAR,PARAM,ITE,UIF = range(5)
    def __init__(self):
        pass

class Formula():
    CHAOS,MIRACLE,UIP,EQN,NEG,ANDLIST,ORLIST,IMPLY,FORALLFORMULA,EXISTFORMULA
    def __init__(self):
        pass

class EConst(Exp):
    def __init__(self,context):
        self.ty = Exp.CONST
        self.context = context

class EVar(Exp):
    def __init__(self,var):
        self.ty = Exp.VAR
        self.var = var 

class EParamr(Exp):
    def __init__(self,paramr):
        self.ty = Exp.PARAM
        self.paramr = paramr

class EIte(Exp,Formula):
    def __init__(self,form,exp1,exp2):
        self.ty = Exp.ITE
        self.form = form
        self.exp1 = exp1 
        self.exp2 = exp2 

class EUIF(Exp):
    def __init__(self,name,*args):
        self.ty = Exp.UIF
        self.name = name
        self.explist = args

class FChaos(Formula):
    def __init__(self):
        self.ty = Formula.CHAOS

class FMiracle(Formula):
    def __init__(self):
        self.ty = Formula.MIRACLE

class FUip(Formula):
    def __init__(self,name,*args):
        self.ty = Formula.UIP
        self.name = name 
        self.explist = args

class FEqn(Formula):
    def __init__(self,e1,e2):
        self.ty = Formula.EQN
        self.exp1 = e1
        self.exp2 = e2 

class FNeg(Formula):
    def __init__(self,f):
        self.ty = Forumla.NEG
        self.formula = f 

class FAndlist(Formula):
    def __init__(self,*args):
        self.ty = Formula.ANDLIST
        self.formulalsit = args

class FOrlist(Formula):
    def __init(self,*args):
        self.ty = Formula.ORLIST
        self.formulalist = args

class FImply(Formula):
    def __init__(self,f1,f2):
        self.ty = Formula.IMPLY
        self.formula1 = f1 
        self.formula2 = f2 

class ForallFormula(Formula):
    def __init__(self,formula,*args)
        self.ty = Formula.FORALLFORMULA
        self.paradeflist = args
        self.formula = formula 


class ExistFormula(Formula):
    def __init__(self,formula,*args):
        self.ty = Formula.EXISTFORMULA
        self.paradeflist = args
        self.formula = formula 

class Statement():
    ASSIGN,PARALLEL= range(2)
    def __init__(self):
        pass

class SAssign(Statement):
    def __init__(self,var,exp):
        self.ty = Statement.ASSIGN
        self.var = var  
        self.exp = exp 

class SParallel(Statment):
    def __init__(self,*args):
        self.ty = Statement.PARALLEL
        self.statementlist = args

class Rule():
    def __init__(self,name,formula,statement,*args):
        self.name = name
        self.formula = formula 
        self.statement = statement
        self.params = args

class Prop():
    def __init__(self,name,formua,*args):
        self.name = name 
        self.formula= formula 
        self.params = args 
i = Intc("1")
print(i.isIntc())