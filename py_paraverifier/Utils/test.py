#!/usr/bin/python
from z3 import *
from pdr import PDR

# SAFE
# This test is a simple program that rotates the variables of three booleans
# The post condition is that at least one of them must be true
# which is inductive because one is initialized to true and never negated, only swapped
def Mutual():
	# Try:n[i] == state.T
	# Crit:And(n[i] == state.C,Not(x))
	# Exit:n[i]==state.E
	# Idle:And(n[i]==state.I,x)
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
	xp = Bool('x\'')
	ip = Int('i\'')
	jp = Int('j\'')
	kp = Int('k\'')
	variables = [i, j, k, x, n]
	primes = [ip, jp, kp, xp]
	init = And(n[i]==state.I,n[j]==state.I, x)
	print('init:',init)
	# trans = Or(Implies(And(n[i]==state.I,x),np[ip] == state.T), Implies(And(n[j]==state.I,x),np[jp] == state.T), Implies(And(n[k]==state.I,x),np[kp] == state.T),
			   # Implies(And(n[i]==state.T,x), And(np[ip] == state.C, xp == Not(x))),Implies(And(n[j]==state.T,x),And(np[jp] == state.C,xp == Not(x))),Implies(And(n[k]==state.T,x),And(n[k] == state.C,xp == Not(x))),
			   # Implies(n[i]==state.C,np[ip] == state.E), Implies(n[j]==state.C,np[jp]==state.E), Implies(n[k]==state.C,np[kp]==state.E),
			   # Implies(n[i]==state.E,And(np[ip] == state.I, xp == x)), Implies(n[j]==state.E,And(np[jp]==state.I,xp == x)), Implies(n[k]==state.E,And(np[kp]==state.I,xp == x)))
	trans = And(n[ip]==state.T)
	print('trans:',trans)
	post = Implies(n[i]==state.C,n[j]!=state.C)
	print('post:',post)
	return variables, primes, init, trans, post


def Swapper():
	x = Bool('x')
	y = Bool('y')
	z = Bool('z')
	xp = Bool('x\'')
	yp = Bool('y\'')
	zp = Bool('z\'')

	variables = [x,y,z]
	primes = [xp,yp,zp]

	init = And(x,Not(y), Not(z))
	trans = And(xp == y, zp == Not(x), yp == z)
	post = Or(x, y, z)
	return (variables, primes, init, trans, post)

# UNSAFE
# A boolean bit vector is initialized with size 8
# to TTTTTTTT. One bit can be flipped per frame.
# The post condition is that at least one bool is True
# which can be violated in 8 frames
def OneAtATime():
	size = 8
	variables = [Bool(str(i)) for i in range(size)]
	primes = [Bool(str(i) + '\'') for i in variables]

	def exclusive(i):
		return And(*[primes[j] == variables[j] for j in range(size) if j != i]+[Not(primes[i] == variables[i])])

	init = And(*[variables[i] for i in range(size-1)] + [(variables[-1])])
	trans = Or(*[exclusive(i) for i in range(size)])
	post = Or(*variables)

	return variables, primes, init, trans, post


# SAFE
# Similar to OneAtATime
# A boolean bit vector is initialized with size 8
# to TTTTTTTT. One bit can be flipped per frame but
# now the two neighbors to it's left must also flip for a total of three.
# The post condition is that at least one bool is True
# which cannot be violated with a bit vector of size 8 and three bits flipped per frame
def ThreeAtATimeEven():
	size = 8
	variables = [Bool(str(i)) for i in range(size)]
	primes = [Bool(str(i) + '\'') for i in variables]

	def triple(i):
		return And(*[primes[j] == variables[j] for j in range(size) if (j != i and j != i-1 and j != i-2)]+\
			[Not(primes[i] == variables[i]),Not(primes[i-1] == variables[i-1]),Not(primes[i-2] == variables[i-2])])

	init = And(*[variables[i] for i in range(size-1)] + [(variables[-1])])
	trans = Or(*[triple(i) for i in range(size)])
	post = Or(*variables)
	return variables, primes, init, trans, post

# UNSAFE
# Three at a time but with an odd length bit vector
# The post condition can now be violated flipping three bits at a time
def ThreeAtATimeOdd():
	size = 9
	variables = [Bool(str(i)) for i in range(size)]
	primes = [Bool(str(i) + '\'') for i in variables]

	def triple(i):
		return And(*[primes[j] == variables[j] for j in range(size) if (j != i and j != i-1 and j != i-2)]+\
			[Not(primes[i] == variables[i]),Not(primes[i-1] == variables[i-1]),Not(primes[i-2] == variables[i-2])])

	init = And(*[variables[i] for i in range(size-1)] + [(variables[-1])])
	trans = Or(*[triple(i) for i in range(size)])
	post = Or(*variables)

	return (variables, primes, init, trans, post)


### More involved examples: ###

# UNSAFE
# Initialize a boolean bitfield to [TTTTTTTTTF]
# Each iteration, each boolean takes the AND of the two bits to its left
# (rolling over at the left back to the right)
# (Frame 1 will look like [FFTTTTTTTT])
# The post condition is simply that at least one boolean be true,
# which can take quite a while to fail depending on the width of the bitfield
#
# This one can take quite a while to run
def BooleanShifter():
	len = 10
	variables = [Bool(str(i)) for i in range(len)]
	primes = [Bool(str(i) + '\'') for i in variables]

	#initialize to something like [T T T T T T T T F]
	init = And(*[variables[i] for i in range(len-1)] + [Not(variables[-1])])
	trans = And(*[primes[i] == And(variables[i-1], variables[i-2]) for i in range(len)])
	post = Or(*variables)

	return (variables, primes, init, trans, post)

# UNSAFE
# Initialize a boolean bitfield [AAAAA BBBBB]
# Each iteration, add the value of BBBBB to AAAAA
# incrementing it
# In this example, BBBBB is 00001 and the postcondition is that
# AAAAA is not 11111, which is unsafe after 16 frames
def BooleanIncrementer():
	len = 8
	variables = [Bool(str(i)) for i in range(len)]
	primes = [Bool(str(i) + '\'') for i in variables]
	init = And(*[Not(variables[i]) for i in range(len-1)] + [variables[-1]])
	len2 = len//2
	def carryout(pos):
		if pos==len/2:
			return False
		else:
			return Or(And(Xor(variables[pos],variables[pos+len2]), carryout(pos+1)),And(variables[pos],variables[pos+len2]))
	trans = And(*[primes[i] == Xor(Xor(variables[i],variables[i+len2]),carryout(i+1)) for i in range(len2)] + [primes[i+len2] == variables[i+len2] for i in range(len2)])
	post = Not(And(*[variables[i] for i in range(len2)]))
	return (variables, primes, init, trans, post)

# SAFE
# Add overflow protection to the previous boolean incrementer
# When the incrementer becomes full, it will not add any more to it
# There is an overflow bit that gets set if there is any carryover from the MSB
# so the postcondition is Not(overflow)
def IncrementerOverflow():
	size = 8
	overflow = Bool('Overflow')
	variables = [Bool(str(i)) for i in range(size)] + [overflow]
	primes = [Bool(str(i) + '\'') for i in variables]
	overflowprime = primes[-1]
	init = And(*[Not(variables[i]) for i in range(size-1)] + [variables[size-1], overflow == False])
	size2 = size //2
	def carryout(pos):
		if pos==size/2:
			return False
		else:
			return Or(And(Xor(variables[pos],variables[pos+size2]), carryout(pos+1)),And(variables[pos],variables[pos+size2]))
	trans = If(And(*[variables[i] for i in range(size2)]), \
		And(*[variables[i] == primes[i] for i in range(len(variables))]),
		And(*[primes[i] == Xor(Xor(variables[i],variables[i+size2]),carryout(i+1)) for i in range(size2)] \
			+ [primes[i+size2] == variables[i+size2] for i in range(size2)] \
			+ [overflowprime==carryout(0)])\
		)
	post = Not(overflow)
	return (variables, primes, init, trans, post)

# SAFE
# Using the same boolean incrementer from before
# In this example, BBB is 010 and the postcondition is that
# AAA is even, which is safe
def EvenIncrementer():
	len = 6
	variables = [Bool(str(i)) for i in range(len)]
	primes = [Bool(str(i) + '\'') for i in variables]
	init = And(*[Not(variables[i]) for i in range(len-2)] + [variables[-2], Not(variables[-1])])
	len2 = len//2
	def carryout(pos):
		if pos==len/2:
			return False
		else:
			return Or(And(Xor(variables[pos],variables[pos+len2]), carryout(pos+1)),And(variables[pos],variables[pos+len2]))
	trans = And(*[primes[i] == Xor(Xor(variables[i],variables[i+len2]),carryout(i+1)) for i in range(len2)] \
		+ [primes[i+len2] == variables[i+len2] for i in range(len2)])
	post = Not(variables[len2-1])
	return (variables, primes, init, trans, post)

tests = {'Mutual':Mutual,'Swapper':Swapper, 'BooleanShifter':BooleanShifter, 'BooleanIncrementer':BooleanIncrementer, 'IncrementerOverflow':IncrementerOverflow,
'EvenIncrementer':EvenIncrementer, 'OneAtATime':OneAtATime, 'ThreeAtATimeEven':ThreeAtATimeEven,
'ThreeAtATimeOdd':ThreeAtATimeOdd}

def listTests():
	for name in tests:
		print(name)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Run tests examples on the PDR algorithm")
	parser.add_argument('-ls', action='store_true')
	parser.add_argument('testname', type=str, help='The name of the test to run', default=None, nargs='?')
	args = parser.parse_args()
	if(args.ls):
		listTests()
	elif(args.testname!=None):
		name = args.testname
		print("=========== Running test", name,"===========")
		solver = PDR(*tests[name]())
		solver.run()
	else:
		for name in tests:
			print("=========== Running test", name,"===========")
			solver = PDR(*tests[name]())
			solver.run()


