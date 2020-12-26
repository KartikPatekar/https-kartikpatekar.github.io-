import numpy as np


##constraint matrices for each of 5 cases
constraints = []
constraints.append(np.asarray([[-3, 1, 3], [0, 5, -3]]))
constraints.append(np.asarray([[0, -5, 1], [-4, -1, 5]]))
constraints.append(np.asarray([[2, -6, -2], [2, 3, -5]]))
constraints.append(np.asarray([[-2, -3, 5], [0, -3, 1]]))
constraints.append(np.asarray([[0, -5, 3], [-2, -1, 3]]))

##All corner points
points = []

##Probability matrices for A,B,C in each of 5 cases
PA=[]
PB=[]
PC=[]

PA.append([0, 1.0/3, 1.0/2])
PB.append([1, -1.0/2, -1.0/2])
PC.append([0, 1.0/2, 0])

PA.append([0, 13.0/16, 3.0/16])
PB.append([1, -3.0/16, -13.0/16])
PC.append([0, -3.0/8, 3.0/8])

PA.append([0, 1.0/2, 1.0/2])
PB.append([1.0/6, -1.0/2, 1.0/3])
PC.append([1.0/2, 0, -1.0/2])

PA.append([0, 3.0/4, 1.0/4])
PB.append([1.0/2, 0, -1.0/2])
PC.append([1.0/2, -1.0/4, -1.0/4])

PA.append([0, 1.0/2, 0])
PB.append([1, -1.0/4, -3.0/4])
PC.append([0, 1.0/4, 1.0/4])

PA = [np.array(P) for P in PA]
PB = [np.array(P) for P in PB]
PC = [np.array(P) for P in PC]


## Given the constraint equations, they intersect the box at 4 positions, out of which only 2 are relevant. We find these 2 points by using fact that useful intercepts
## lie on box [0,1]x[0,1] edge which containes the useful box corner
def findintercept(constraints, a, b):
	interceptpts = []

	for i in range(2):
		j = 1-i

		n = -1.0/constraints[i,2]*(constraints[i,0] + constraints[i,1]*a)

		X = np.array([1, a , n])

		Y = np.dot(constraints[j], X)

		if(Y >=0 and n >=0 and n <= 1):
			interceptpts.append([a,n])

	for i in range(2):
		j = 1-i

		m = -1.0/constraints[i,1]*(constraints[i,0] + constraints[i,2]*b)

		X = np.array([1, m , b])
		Y = np.dot(constraints[j], X)

		if(Y>=0  and m >=0 and m <= 1):
			interceptpts.append([m,b])

	return interceptpts



for i in range(5):
	
	points.append([])

	# Working in x_A-x_B space, there would be one corner of box [0,1]x[0,1] which would be a constrained region corner as well. 
	for a in range(2):
		for b in range(2):
			X = np.array([1 , a, b])
			Y = np.matmul(constraints[i], X)

			if (Y[0] >=0 and Y[1] >= 0):
				points[-1].append([a,b])

	interceptpts = []
	# Find region corner points which appear at constraint's intersection with box [0,1]x[0,1]
	for p in points[-1]:
		a = p[0]
		b = p[1]

		interceptpts = findintercept(constraints[i], a,b)

	points[-1] = points[-1] + interceptpts

	# find region corner point occuring at intersection of 2 constraints. 
	Y = constraints[i][: , 0]
	M = constraints[i][: , 1:]
	Minv = np.linalg.inv(M)
	X = -np.matmul(Minv, Y)
	points[-1].append(X.tolist())

points = [np.asarray(pts) for pts in points]

points_m1 = []

#for every corner point (x_A, x_B) in region i, we compare the probability of B if it instead lied in region j.  
def checkB(constraints, a, PB_i, PB_vec):
	
	for i in range(2):
		j=1-i
		m = -1.0/constraints[i,2]*(constraints[i,0] + constraints[i,1]*a)

		if(m>1):
			m=1
		if(m<0):
			m=0

		X = np.asarray([1, a, m])
		Y = np.matmul(constraints, X)


		if(Y[0] < 0 or Y[1] < 0):
			continue

		PB_j = np.dot(PB_vec, X)

		if(PB_j>PB_i):
			return True

	return False


#We now remove region corner points which are optimal choices for B or C.
for i in range(5):

	points_m1.append([])		# this variable will contain only useful points. 

	for p in points[i]:
		rejectp = False

		if(p[0] >0.5):			
			continue;

		for j in range(5):		#compare with cases other than i

			if(rejectp == True):
				break

			if(j==i):
				continue

			X = np.asarray([1, p[0], p[1]])			
			Y = np.matmul(constraints[j], X)	

			if(Y[0] < 0  or Y[1]< 0):
				continue

			#look at optimality of C's choice
			if( np.dot(PC[j], X) > np.dot(PC[i], X) ):
				rejectp = True
				break

			#look at optimality of B's choice, comparing it with possibility if B lied in region j.
			if(checkB(constraints[j], p[0], np.dot(PB[i], X), PB[j])==True):
				rejectp = True
				break

		if(rejectp == False):
			points_m1[-1].append(p.tolist())

		
maxpA = 0
xa = 0

#Now we find point with maximum probability of A
for i in range(5):
	for p in points_m1[i]:
		X = np.asarray([1, p[0], p[1]])
		
		if(np.dot(PA[i], X) > maxpA):
			maxpA = np.dot(PA[i], X)
			xa = p[0]

print(xa)