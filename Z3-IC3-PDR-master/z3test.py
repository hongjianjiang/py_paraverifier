from z3 import *

state = Datatype('state')
state.declare('I')
state.declare('T')
state.declare('C')
state.declare('E')
state = state.create()
n = Array('n',IntSort(),state)
x = Bool('x')
i = Int('i')
j = Int('j')
k = Int('k')
solve(n[i]==state.I)
trans = Or(n[i] == state.T, n[j] == state.T, n[k] == state.T,
           And(n[i] == state.C, Not(x)), And(n[j] == state.C, Not(x)), And(n[k] == state.C, Not(x)),
           n[i] == state.E, n[j] == state.E, n[k] == state.E,
           And(n[i] == state.I, x), And(n[j] == state.I, x), And(n[k] == state.I, x))