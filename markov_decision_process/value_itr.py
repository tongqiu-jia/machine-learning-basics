import numpy as np
import copy

#load raw data from file
a1 = np.loadtxt("prob_a1.txt",dtype=[('num1',int),('num2',int),('num3',float)])
a2 = np.loadtxt("prob_a2.txt",dtype=[('num1',int),('num2',int),('num3',float)])
a3 = np.loadtxt("prob_a3.txt",dtype=[('num1',int),('num2',int),('num3',float)])
a4 = np.loadtxt("prob_a4.txt",dtype=[('num1',int),('num2',int),('num3',float)])
rewards = np.loadtxt("rewards.txt",dtype=int)

#process data into 3darray
trans_matrix = np.zeros((81,81,4))
for entry in a1:
	trans_matrix[entry[0]-1][entry[1]-1][0] = entry[2]
for entry in a2:
	trans_matrix[entry[0]-1][entry[1]-1][1] = entry[2]
for entry in a3:
	trans_matrix[entry[0]-1][entry[1]-1][2] = entry[2]
for entry in a4:
	trans_matrix[entry[0]-1][entry[1]-1][3] = entry[2]

#some constants
gamma = 0.9925
S = len(rewards) #number of states S=81
A = 4 #numbr of actions 

#initialize all states to 0 at 0th iteration 
V = np.zeros(S)

#iteration step
for iteration in range(0,3000):
	V_copy = copy.deepcopy(V)
	for i in range(0,S):
		sum1,sum2,sum3,sum4 = 0.0,0.0,0.0,0.0
		for j in range(0,S):
			sum1 += V_copy[j]*trans_matrix[i][j][0]
			sum2 += V_copy[j]*trans_matrix[i][j][1]
			sum3 += V_copy[j]*trans_matrix[i][j][2]
			sum4 += V_copy[j]*trans_matrix[i][j][3]
		V[i] = rewards[i] + gamma * max([sum1,sum2,sum3,sum4])

#compute optimal policy
pi = np.zeros(S)
for k in range(0,S):
	sum1,sum2,sum3,sum4 = 0.0,0.0,0.0,0.0
	for l in range(0,S):
		sum1 += V[l]*trans_matrix[k][l][0]
		sum2 += V[l]*trans_matrix[k][l][1]
		sum3 += V[l]*trans_matrix[k][l][2]
		sum4 += V[l]*trans_matrix[k][l][3]
	pi[k] = np.argmax([sum1,sum2,sum3,sum4])

#write to file
f = open('result.txt', 'w')
f.write("The nonzero value of optimal state value function: \n")
for z in range (0,S):
	if V[z] != 0:
		f.write('V('+str(z+1)+') = '+str(V[z])+'\n')
f.write('The optimal policy: \n')
for m in range(0,len(pi)):
	#if pi[m] == 0:
	#	f.write(str(m+1)+' West\n')
	if pi[m] == 1:
		f.write(str(m+1)+' North\n')
	elif pi[m] == 2:
		f.write(str(m+1)+' East\n')
	elif pi[m] == 3:
		f.write(str(m+1)+' South\n')
f.close()
