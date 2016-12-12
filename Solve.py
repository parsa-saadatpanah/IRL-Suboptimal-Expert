import math
import numpy
from scipy.optimize import minimize
trajectory = []
features = []
Cf = {}
Cs = []
def read():
	global trajectory
	global features
	global Cf
	global Cs
	tFile = open('trajectory','r')
	fFile = open('features','r')
	trajectory = []
	for line in tFile:
		l = line.split()
		t = [int(i) for i in l]
		trajectory.append(t)

	features = []
	for line in fFile:
		l = line.split()
		t = [float(i) for i in l]
		features.append(t)

	Cs = [0.0 for i in range(len(features))]
	for t in trajectory:
		for state in t:
			Cs[state] = Cs[state] + 1
	s = sum(Cs)
	for i in range(len(Cs)):
		Cs[i] = Cs[i]/s
	# print(Cs)

	
	#this is wrong!!!
	# for f in features:
	# 	ff = repr(f)
	# 	if ff in Cf:
	# 		Cf[ff] = Cf[ff] + 1
	# 	else: 
	# 		Cf[ff] = 1
	#return trajectory, features

def getP(theta):
	global trajectory
	global features
	global Cf
	global Cs
	p = []
	z = 0.0
	for t in trajectory:
		exponent = 0.0
		for state in t:
			# exponent = exponent + numpy.dot(features[state], theta)*Cf[repr(features[state])]
			exponent = exponent + numpy.dot(features[state], theta)*Cs[state]
			# exponent = exponent + numpy.dot(features[state], theta)
		prob = math.exp(exponent)
		if prob==0:
			print exponent
		p.append(prob)
		z = z+prob
	for i in range(len(p)):
		p[i] = p[i]/z
	return p

def L(theta):	
	likeliHood = 0.0
	p = getP(theta)	
	# print(p)
	for prob in p:
		likeliHood = likeliHood + math.log(prob)
	print likeliHood
	return likeliHood*-1

def L_der(theta):
	global features
	global trajectory
	p = getP(theta)
	fAvg = [0.0 for i in range(len(features[0]))]
	fProb = [0.0 for i in range(len(features[0]))]
	for path_id in range(len(trajectory)):
		fPath = [0.0 for i in range(len(features[0]))]
		for state in trajectory[path_id]:
			fPath = numpy.add(fPath, features[state])
		fAvg = numpy.add(fAvg, fPath)
		fPath = numpy.multiply(p[path_id], fPath)
		fProb = numpy.add(fProb, fPath)
	fAvg = numpy.multiply(float(1)/len(trajectory) ,fAvg)
	# print(p)
	ans = numpy.subtract(fAvg, fProb)	
	ans = numpy.multiply(-1.0, ans)
	return ans


def solve():
	read()
	x0 = [-1 for i in range(len(features[0]))]
	res = minimize(L, x0, method='BFGS', jac=L_der, options={'disp': True})
	# print(res.x)
	return res.x













