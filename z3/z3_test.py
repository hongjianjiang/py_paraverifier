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
# print(formula)
    # 'And([ ni == c,t==c]) '
    #     'assert (and (= (select N i) c) (= (t c)'
# formula=z3.Z3_solver_from_string('And([ni == c,t==c])')
# z3.Optimize.from_string('assert (= (ni) t')
# s.from_string('And([ni == c,t==c])')
s.from_string('(declare-datatypes () ((state I T C E ))) (declare-const n (Array Int state)) (declare-const x Bool) (declare-const y Bool) (declare-const i Int) (assert (and (= T C) (= (select n i) C)))')
              # '(assert (and (= (select n i) C)'
              # '             (= T C)         '
              # ')'
              # ')')
# s.from_string('(declare-datatypes () ((state I T C E ))) (declare-const n (Array Int state)) (declare-const x Bool) (declare-const y Bool) (declare-const i Int) (assert (= T C))')

print(s.check())
# !(T=C & n[2]=C)
# s.add(formula)
# print(s.check())
# print("====================")
# x = Int('x')
# print(is_expr(State.I))
# print(N[x])
# print(Select(N,x))
# print(Store(N,x,State.I))
# print(simplify(Select(Store(N,x,State.I),2)))

