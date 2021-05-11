import ply.yacc as yacc
 
 # Get the token map from the lexer.  This is required.
from ocamlclex import tokens
literals = ['=','+','-','*','/', '(',')','{','}']

t_ignore = " \t"
names = {} 
types = {}
consts = {}
def p_const_type(p):
    'expression :  const ID  COLON NUMBER SEMICOLON'
    consts[p[2]] = p[4]
    print(p[2],p[4])

def p_const_var(p):
    'expression :  type ID  COLON enum LBPAREN ID RBPAREN SEMICOLON'
    types[p[1]]=(p[6:])
    print(types)

def p_expression_term(p):
    'expression : NUMBER'
    p[0] = p[1]
    print('number',p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = p[1]
    print('ID',p[1])

def p_statement_assign(p):
    'statement : ID EQ NUMBER SEMICOLON'
    print('test')

def p_statement_expr(p):
    'statement : expression'
    print(p[1])


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
 
yacc.yacc()
 
while 1:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)