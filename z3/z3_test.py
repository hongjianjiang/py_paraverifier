from z3 import *

State = Datatype('State')
State.declare('I')
State.declare('T')
State.declare('C')
State.declare('E')
State = State.create()


# i = Int("i")
# I = IntSort()
# N = Array('N', I, State)
# x = Bool('x')
# c = State.C
# ni = Select(N,i)
# t = State.T
x = Bool('x')
y = Bool('y')
s = Solver()
print(s.check())

