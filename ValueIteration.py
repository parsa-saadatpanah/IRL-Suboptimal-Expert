import random

def readFile(f):
	stateCount = int(f.readline())
	actionCount = int(f.readline())
	T = [[0 for i in range(actionCount)] for j in range(stateCount)]
	for i in range(stateCount*actionCount):
		l = f.readline()
		T[int(l.split()[0])][int(l.split()[1])] = int(l.split()[2])
	terminals = []
	# for i in range(stateCount):
	# 	ss = T[i][0]
	# 	good = True
	# 	for j in range(actionCount):
	# 		if T[i][j] != ss:
	# 			good=False
	# 	if good:
	# 		terminals.append(i)
	r = [0 for i in range(stateCount)]
	for i in range(stateCount):
		l = f.readline()
		r[int(l.split()[0])] = int(l.split()[1])
	return stateCount, actionCount, T, terminals, r

def valueIteration(T, r, terminals):
	worst = min(r) - abs(min(r))*len(r)
	V = [worst for i in range(len(r))]
	for state in terminals:
		V[state] = r[state]

	for iteration in range(len(r)+10):
		Vnew = [worst for i in range(len(r))]
		for state in terminals:
			Vnew[state] = r[state]
		for i in range(len(Vnew)):
			if i in terminals:
				continue
			best = V[T[i][0]]
			for action in range(len(T[0])):
				best = max(best, V[T[i][action]])
			Vnew[i] = best + r[i]
		different = False
		for i in range(len(V)):
			if V[i]!=Vnew[i]:
				different = True
			V[i] = Vnew[i]
		if different == False:
			break
	return V

def policy(T, V, terminals):
	P = [0 for i in range(len(V))]
	for i in range(len(V)):
		if i in terminals:
			P[i] = -1
			continue
		best = 0
		for action in range(len(T[i])):
			if V[T[i][action]] > V[T[i][best]]:
				best = action
		P[i] = best
	return P	

def terajectory(T, P, startState):
	trej = []
	now = startState
	trej.append(now)
	# print(P)
	while(P[now]!=-1):
		# if now == T[now][P[now]]:
		# 	print(now)
		# 	raw_input("Press Enter to continue...")
		now = T[now][P[now]]
		trej.append(now)
	return trej

def noise(r, terminals, accuracy):
	rOut = [0 for i in range(len(r))]
	for state in range(len(r)):
		if (state in terminals) or random.random()<=accuracy:
			rOut[state] = r[state]
		else:
			rOut[state] = -1
	return rOut

def optimalTrej(rNew):
	# out = open('trajectory', 'w')
	stateCount, actionCount, T, terminals, r = readFile(open('WorldData','r'))
	if rNew is None:
		rNew = r

	V = valueIteration(T, rNew, terminals)
	P = policy(T,V,terminals)
	trej = terajectory(T,P,0)
	return trej

def compare(T1, T2):
	stateCount, actionCount, T, terminals, r = readFile(open('WorldData','r'))
	T1Val = 0
	T2Val = 0
	for i in T1:
		T1Val = T1Val + r[i]
	for i in T2:
		T2Val = T2Val + r[i]
	return T1Val, T2Val


def runSuboptimal():
	stateCount, actionCount, T, terminals, r = readFile(open('WorldData','r'))
	expertCount = 1000
	out = open('trajectory','w')
	for i in range(expertCount):
		print(i)
		# terminals = [random.randint(0, stateCount-1)]
		terminals = [random.randint(stateCount-1, stateCount-1)]
		rSubOptimal = noise(r, terminals, 0.9)
		V = valueIteration(T,rSubOptimal, terminals)
		P = policy(T,V,terminals)				
		trej = terajectory(T,P, 0)
		# trej = terajectory(T,P, random.randint(0, stateCount-1))
		for i in trej:
			if i!=0:
				out.write(' ')
			out.write(str(i))
		out.write('\n')

