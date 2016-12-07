import ValueIteration
import Solve
import random
import matplotlib.pyplot as plt

def readGrid():
	f = open('Grid1', 'r')
	x = int(f.readline())
	y = int(f.readline())
	r = [[0 for i in range(y)] for j in range(x)]
	i = 0
	for line in f:
		l = line.split()
		for j in range(y):
			r[i][j] = l[j]
		i = i+1
	# print(r)
	return r
def writeGrid(r):
	f = open('WorldData','w')
	# f.write('State Count=\n')
	stateCount = len(r)*len(r[0])
	f.write(str(stateCount)+'\n')
	# f.write('Action Count=\n')
	actionCount = 4
	f.write(str(actionCount)+'\n')
	# f.write('Transtions= (s,a,s\')\n')
	T = [[0 for i in range(actionCount)] for j in range(stateCount)]
	for i in range(len(r)):
		for j in range(len(r[0])):
			T[i*len(r[0])+j][0] = (i+1)*len(r[0])+j
			T[i*len(r[0])+j][1] = (i)*len(r[0])+j+1
			T[i*len(r[0])+j][2] = (i-1)*len(r[0])+j
			T[i*len(r[0])+j][3] = (i)*len(r[0])+j-1
	for j in range(len(r[0])):
		T[(len(r)-1)*len(r[0])+j][0] = (len(r)-1)*len(r[0])+j
		T[0*len(r[0])+j][2] = 0*len(r[0])+j
	for i in range(len(r)):
		T[i*len(r[0])+len(r[0])-1][1] = (i)*len(r[0])+len(r[0])-1
		T[i*len(r[0])+0][3] = (i)*len(r[0])+0
	# T[len(r)*len(r[0])-1][0] = len(r)*len(r[0])-1
	# T[len(r)*len(r[0])-1][1] = len(r)*len(r[0])-1
	# T[len(r)*len(r[0])-1][2] = len(r)*len(r[0])-1
	# T[len(r)*len(r[0])-1][3] = len(r)*len(r[0])-1
	for s in range(len(T)):
		for a in range(len(T[0])):
			f.write(str(s)+' '+str(a)+' '+str(T[s][a])+'\n')

	# f.write('Rewards=\n')
	for i in range(len(r)):
		for j in range(len(r[0])):
			f.write(str(i*len(r[0])+j)+' '+str(r[i][j])+'\n')
	
	# features
	features = open('features', 'w')
	for i in range(len(r)*len(r[0])):
		# features.write(str(int(i/len(r[0]))/float(len(r)))+' '+str((i%len(r[0]))/float(len(r[0]))))
		for j in range(len(r)*len(r[0])):
			if j!=0:
				features.write(' ')
			if i==j:
				features.write('1')
			else:
				features.write('0')
		features.write('\n')

def terajectoryToGrid():
	r = readGrid()
	x = len(r)
	y = len(r[0])
	G = [ [0 for i in range(y)] for j in range(x)]
	f = open('trajectory','r')
	t = []
	for line in f:
		for i in line.split():
			t.append(int(i))
	for state in t:
		i = int(state/y)
		j = state%y
		G[i][j] = G[i][j]+1
	f = open('terajGrid', 'w')
	for i in range(x):
		for j in range(y):
			f.write(str(G[i][j])+' ')
		f.write('\n')

def rewardToGrid(theta):
	r = readGrid()
	x = len(r)
	y = len(r[0])
	G = [ [0 for i in range(y)] for j in range(x)]
	for i in range(x):
		for j in range(y):
			# G[i][j] = i*theta[0]+j*theta[1]
			G[i][j] = theta[i*y+j]
	plt.imshow(G, cmap='hot', interpolation='nearest')
	# plt.show()
	plt.savefig('LearnedGrid.jpg')
	f = open('rewardGrid', 'w')
	for i in range(x):
		for j in range(y):
			f.write(str(G[i][j])+' ')
		f.write('\n')
	return G

def normalize(x):
	m = max(x)
	x2 = [i-m-1 for i in x]
	return x2




writeGrid(readGrid())
ValueIteration.runSuboptimal()
terajectoryToGrid()
theta = Solve.solve()
print(theta)
# x2 = normalize(x)
r2 = rewardToGrid(theta)
# TOptimal = ValueIteration.optimalTrej(None)
# TLearn = ValueIteration.optimalTrej(x2)
# print(ValueIteration.compare(TOptimal, TLearn))
