import numpy as np
import matplotlib.pyplot as plt

num=1000000
y1=0.3*np.ones(num)
y2=0.25*np.ones(num)
y3=0.45*np.ones(num)

dt=0.001

def check(y):
	count=0

	on=np.ones(num)
	if ((y-0.01)*(0.99-y)>0).any():
		return 0

	# for i in range(num):
	# 	if arr[i]>0.01 and arr[i]<0.99:
	# 		return 0

	return 1

def countfunc(arr):
	count=0
	for i in range(num):
		if arr[i]>=0.99:
			count=count+1;

	return count
	
def dW(delta_t): 
    return np.random.normal(loc = 0.0, scale = np.sqrt(delta_t))

def genw():
	w=np.random.randint(3, size=num)
	w1=0.5*(w-1)*(w-2)
	w2=-w*(w-2)
	w3=0.5*w*(w-1)
	return w1,w2,w3

on=np.ones(num)

while check(y1)==0 :
	w1,w2,w3=genw()
	dw=dW(dt)
	y1=y1+2.0*y1*(w1-w1*y1-w2*y2-w3*y3)*dw
	y2=y2+2.0*y2*(w2-w1*y1-w2*y2-w3*y3)*dw
	y3=y3+2.0*y3*(w3-w1*y1-w2*y2-w3*y3)*dw


noofplus=countfunc(y1)
print(noofplus, 1.0*noofplus/num)


