# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LMPAREN',
    'RMPAREN',
    'LBPAREN',
    'RBPAREN',
    'SENDTO',
    'EQ',
    'COLON',
    'LET',
    'ID',
    'ruleset',
    'const',
    'type',
    'var',
    'rule',
    'endruleset',
    'startstate',
    'endstartstate',
    'invariant',
    'do',
    'ASSIGN',
    'begin',
    'end',
    'for',
    'endfor',
    'SEMICOLON',
    'IMPLY',
    'DQM',
    'enum'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LMPAREN = r'\['
t_RMPAREN = r'\]'
t_LBPAREN = r'\{'
t_RBPAREN = r'\}'
t_SENDTO = r'->'
t_COLON = r':'
t_ASSIGN = r':='
t_EQ = r'\='
t_SEMICOLON = r'\;'
t_IMPLY = r'\==>'
t_DQM = r'\"'
reserved = {
    'const': 'const',
    'type': 'type',
    'var': 'var',
    'ruleset': 'ruleset',
    'rule': 'rule',
    'endruleset': 'endruleset',
    'startstate': 'startstate',
    'endstartstate': 'endstartstate',
    'invariant': 'invariant',
    'do': 'do',
    'begin': 'begin',
    'end': 'end',
    'for': 'for',
    'endfor': 'endfor',
    'enum':'enum'
}


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
data = '''
ruleset i: client do 
rule "try" n[i] = I ==> begin 
    n[i]:= T;
end;
startstate
begin
for i : client do 
n[i] := I;
endfor;
endstartstate;
 '''
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)