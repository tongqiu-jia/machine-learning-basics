import numpy
import matplotlib.pyplot as plt

#read initial state distribution from file
ini_state_distribtion = numpy.loadtxt("initialStateDistribution.txt")
#read transition matrix from file
trans_matrix = numpy.loadtxt("transitionMatrix.txt")
#read emission matrix from file
emission_matrix = numpy.loadtxt("emissionMatrix.txt")
#read observations from file
observations = numpy.loadtxt("observations.txt",dtype=int)

#some constants
n = 26 #number of hidden states
T = len(observations) #number of observations 

#initialize to all zeros
L = numpy.zeros((n,T))
L_ = numpy.zeros((1,T))

#base case: 1st column
log_pi = numpy.log(ini_state_distribtion)
log_bi = numpy.log(emission_matrix)
log_aij = numpy.log(trans_matrix)

#1st column of matrix L
if observations[0] == 0:
	L[:,0] = log_pi + log_bi[:,0]
else:
	L[:,0] = log_pi + log_bi[:,1]

#get argmax
L_[:,0] = numpy.argmax(L[:,0])

#fill matrix L for time t to t+1
for i in range(1,T):
	for j in range(n):
		L[j,i] = numpy.max(L[:,i-1] + numpy.transpose(log_aij[j,:]))
	if observations[i] == 0:
		L[:,i] = L[:,i] + log_bi[:,0]
	else:
		L[:,i] = L[:,i] + log_bi[:,1]
	#get argmax
	L_[:,i] = numpy.argmax(L[:,i])

plt.plot(L_[0])
plt.grid(True)
plt.yticks(numpy.arange(0, n, 1))
plt.show()
