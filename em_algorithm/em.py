import math
T = 267
n = 23
num_itr = 512

#get x from file
file = open("hw6_x.txt")
master_list_x = []
for line in file:
	list_x = line.split() #this yields a string list with'\n'
	list_x[-1] = list_x[-1].strip() #get ride of '\n'
	list_x =[int(i) for i in list_x] #convert to list of int
	master_list_x.append(list_x)
file.close

#get y from file
file = open("hw6_y.txt")
list_y = []
for line in file:
	list_temp = line.split() #yields list of string
	list_y.append(list_temp[0])
list_y = [int(j) for j in list_y] #convert to list of int
file.close

#initialize CPT
cpt_x = [None] * n
for i in range(0,n):
	cpt_x[i] = 1/(2*n)

#report log-likelihood and number of mistakes for each iteration 
def iteration_report(cpt):
	L = 0.0 #log-likelihood
	M = 0 #number of mistakes
	for i in range (0, T): #sum over all T
		temp = 1.0
		for j in range(0, n):
			temp *= math.pow(1-cpt[j],master_list_x[i][j])	
		#choose base on y = 0 or y = 1
		if list_y[i] is 0:
			#false positive,mistake count increments
			if ((1-temp) >= 0.5):
				M += 1 
			temp = math.log(temp)	
		if list_y[i] is 1:
			#false negative, mistake count increments
			if ((1-temp) <= 0.5):
				M += 1
			temp = math.log(1 - temp)
		L += temp
	L = L/T #normalize over T
	print ("The numer of mistakes are", M)
	print ("The log-likelihood is ","%.4f" %L)

#updates cpt 	
def cpt_update(old_cpt):
	new_cpt = [None] * n
	for i in range (0, n): #there are n=23 entries in new cpt
		Ti = 0
		for j in range (0,T):
			Ti += master_list_x[j][i]
		#done with Ti
		temp_sum = 0.0 #temp to take sum over T
		for k in range (0,T):
			numerator = list_y[k] * old_cpt[i] * master_list_x[k][i]
			demominator = 0
			temp = 1.0
			for l in range (0,n):
				temp *= math.pow(1- old_cpt[l], master_list_x[k][l])
			demominator = 1 - temp
			temp_sum += numerator/demominator
		new_cpt[i] = (1/Ti) * temp_sum
	return new_cpt

#iterate and print results
print("Iteration",'0')
iteration_report(cpt_x)
cpt = cpt_x
for i in range (1,num_itr+1):
	print("Iteration",i)
	cpt = cpt_update(cpt)
	iteration_report(cpt)
for j in range (0,len(cpt)):
	print("p",j+1,"=","%.6f" % cpt[j])