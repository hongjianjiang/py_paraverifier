# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------
 
import sys
if sys.version_info[0] >= 3:
    raw_input = input
 
tokens = (
    'NAME','NUMBER','CONST','TYPE','ENUM','VAR','ARRAY','OF','RULESET','DO','RULE','BEGIN','END','ENDRULESET','FOR','ENDFOR',"STARTSTATE",'ENDSTARSTATE',
    'ID','INVARIANT'
    )
 
literals = ['=','+','-','*','/', '(',')']
 
# Tokens
 
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_CONST = r'const'
t_TYPE = r'type'
t_ENUM = r'enum'
t_VAR = r'var'
t_ARRAY = r'array'
t_OF = r'of'
t_RULESET = r'ruleset'
t_DO = r'do'
t_RULE = r'rule'
t_BEGIN = r'begin'
t_END = r'end'
t_ENDRULESET = r'endruleset'
t_FOR = r'for'
t_ENDFOR = r'endfor'
t_STARTSTATE = r'startstate'
t_ENDSTARSTATE = r'endstartstate'
t_INVARIANT = r'invariant'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
 
t_ignore = " \t"
 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()
 
# Parsing rules
 
precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )
 
# dictionary of names
names = { }
 
def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]
 
def p_statement_expr(p):
    'statement : expression'
    print(p[1])
 
def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]
 
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]
 
def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]
 
def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]
 
def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0
 
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
 
import ply.yacc as yacc
yacc.yacc()
 
while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)