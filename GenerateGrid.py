import random
import matplotlib.pyplot as plt


def generate1():
	f = open('Grid1', 'w')
	x = 15
	y = 10
	rate = 0.4
	f.write(str(x)+'\n')
	f.write(str(y)+'\n')
	r = [[-1*(i+j)-1 for i in range(y)] for j in range(x)]
	# r = [[-1 for i in range(y)] for j in range(x)]
	# print(r)
	# for i in range(x):
	# 	for j in range(y):
	# 		if i==x-1 and j==y-1:
	# 			continue
	# 		rand = random.random()
	# 		if rand<rate:
	# 			r[i][j]= random.randint(-10,-5)
	plt.imshow(r, cmap='hot', interpolation='nearest')
	plt.show()
	plt.savefig('OriginalGrid.jpg')
	for i in range(x):
		for j in range(y):
			if j!=0:
				f.write(' ')
			f.write(str(r[i][j]))
		f.write('\n')
	

	
	
			

generate1()

