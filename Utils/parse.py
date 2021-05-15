# Author: Hongjian Jiang

from lark import Lark, Transformer, v_args, exceptions
from Utils.type import *

grammar = r"""
    ?const: SIGNED_NUMBER -> intc
        | ESCAPED_STRING  -> strc 
        | "true" -> true
        | "false" -> false 
        
    ?var: WORD  [("_" WORD)*|(SIGNED_NUMBER "_" WORD)* | ] -> var
    ?var1 : var WORD -> var1 
    //?paramr : WORD -> paramref
         
    ?expression:  const -> econst
        | WORD -> econst
        | var1 -> evar
        | "if" formula "then" expression "else" expression -> eite
//        | (WORD WORD) -> eparamr
        
    ?statement: "'" expression "'" ":"  "'" expression "'" -> sassign
        | statement "," statement -> sparallel
    
    ?state: WORD -> intc
    ?datalist : "'" WORD "'" ("," "'" WORD "'")* -> datalist
    ?formula: "true" -> fchaos
        | "false"    -> fmiracle
        |  expression "=" expression  -> feqn
        |  "~" "(" formula ")" -> fneg
        | formula "&" formula -> fandlist
        | formula "|" formula -> forlist
        | formula "->" formula -> fimply
        
    ?rule: "{" "'" "name':" "'" WORD "'" "," "'" "var" "'" ":" "\"" "[" datalist "]" "\"" "," "'guard'" ":" "'"  formula "'" "," "'assign'"  ":" "{" statement "}" "}" ->  rule
    
    ?prop: "{" "'" "vars" "'" ":"  "[" datalist "]"  "," "'prop':" "'" formula  "'" "}"-> prop
    
    ?init: "{" "'" "var" "'" ":"  "[" datalist "]"  "," "'guard':" "'" formula  "'" "}"-> startstate
    
    
    int : SIGNED_NUMBER
    string : ESCAPED_STRING
    %import common.WORD
    %import common.WS
    %import common.INT
    %import common.SIGNED_NUMBER
    %import common.ESCAPED_STRING
    %ignore WS
"""


@v_args(inline=True)
class ParaverifierTransformer(Transformer):
    def __init__(self):
        pass

    def intc(self, s):
        return Intc(s)

    def strc(self,s):
        return Strc(str(s))

    def true(self):
        return Boolc("True")

    def false(self):
        return Boolc("False")

    def typedef(self,n,*args):
        return Typedef(n,args)

    def paramdef(self,n,tn):
        return Paramdef(n,tn)

    def paramref(self,n):
        return Paramref(n)

    def paramfix(self,vn,tn,value):
        return Paramfix(vn,tn,value)

    def vardef(self,arn,tyn,*args):
        return Vardef(arn,args,tyn)

    def var(self,*args):
        # print('var:',args[0])
        return Var(args[0])

    def var1(self,*args):
        # print('var1:',args)
        return EVar(args[0], args[1])

    def evar(self,*args):
        # print('evar:',args)
        return args[0]

    def econst(self,context):
        return EConst(context)

    # def eword(self,*args):
    #     return EVar(args[0],args[1])

    def eparamr(self,p):
        return EParamr(p)

    def fchaos(self):
        return FChaos()

    def fmiracle(self):
        return FMiracle()

    def eite(self,*args):
        return EIte(args[0],args[1],args[2])

    def euif(self,n,*args):
        return EUIF(n,args)

    def fuip(self,e1,e2):
        return FUip(e1,e2)

    def feqn(self,*args):
        # print(args)
        return FEqn(args[0], args[1])

    def fneg(self,f):
        return FNeg(f)

    def fandlist(self,*args):
        return FAndlist(args)

    def forlist(self,*args):
        return FOrlist(args)

    def fimply(self,f1,f2):
        return FImply(f1,f2)

    def forallformula(self,f,*args):
        return ForallFormula(f,args)

    def existformula(self,f,*args):
        return ExistFormula(f,args)

    def sassign(self,v,e):
        return SAssign(v,e)

    def sparallel(self,*args):
        return SParallel(args)

    def rule(self,*args):
        # print(args)
        # args1=str(args[0])
        return Rule(args[0],args[2],args[3],args[1])

    def prop(self,*args):
        # print(args)
        return Prop(args[1],args[0])

    def startstate(self,*args):
        return StartState(args[1],args[0])

    def datalist(self,*args):
        result = []
        for i in range(len(args)):
            result.append(str(args[i]))
        return result


def get_parser_for(start):
    return Lark(grammar, start=start, parser="lalr", transformer=ParaverifierTransformer())


const_parser = get_parser_for('const')
vars_parser = get_parser_for("var")
# param_parse = get_parser_for('paramr')
exp_parser = get_parser_for('expression')
state_parser = get_parser_for('state')
form_parser = get_parser_for('formula')
statement_parser = get_parser_for('statement')
rule_parser = get_parser_for('rule')
prop_parser = get_parser_for('prop')
# rule_parser = get_parser_for("rule")
# prop_parser = get_parser_for("prop")
init_parser = get_parser_for('init')

def parse_const(s):
    """Parse a type."""
    T = const_parser.parse(s)
    return T
def parse_vars(s):
    """Parse a var."""
    T = vars_parser.parse(s)
    return T
def parse_exp(s):
    """Parse a exp."""
    T = exp_parser.parse(s)
    return T
def parse_state(s):
    """Parse a state."""
    T = state_parser.parse(s)
    return T

def parse_form(s):
    """Parse a formula."""
    T = form_parser.parse(s)
    return T
def parse_statement(s):
    """Parse a rule."""
    T = statement_parser.parse(s)
    return T

def parse_rule(s):
    """Parse a rule."""
    T = rule_parser.parse(s)
    return T

def parse_prop(s):
    """Parse a prop."""
    T = prop_parser.parse(s)
    return T

def parse_init(s):
    T = init_parser.parse(s)
    return T

if __name__ == '__main__':
    text3 = r'I'
    formula = '~ (n[i] = E & n[j] = E)'
    # print(parse_state(text3))
    text = r"{'vars': ['i', 'j'], 'prop': '~ (n[i] = E & n[j] = E)'}"
    text1 = r"{'vars': ['i', 'j'], 'prop': '~ (n i = C & n j = C)'}"
    text2 = r"{'var': 'k', 'guard': 'n[k] = I', 'assign': {'n[k]': 'T'}}"
    assign = r"'n k': 'T'"
    prop = r"{'vars': ['i', 'j'], 'prop': '~ (n i  = C & n j  = C)'}"
    # rule = r"{'name': 'Idle','var': "['i']", 'guard': 'n i  = E','assign': {'n i ': 'I','x': 'true'}}"
    print(parse_prop(prop))
    # print(parse_rule(text2).getArgs()[0])
    # print(parse_rule(rule))
    # print(parse_statement(assign))