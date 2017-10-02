import math
from data import loadData, critics, loadNewData

# Takes 3 parameters, data, names of the items
def euclid(itemData,ione,itwo):
	# Get what items are shared between two movies
	shared = {}
	total = 0 
	#print shared
	for person in itemData[ione]:
		if person in itemData[itwo]:
			shared[person] = 1
			# Calculate using Euclid's formula
			total += (itemData[ione][person]-itemData[itwo][person])**2

		#print shared

	# If nothing common return 0
	if len(shared) == 0:
		return 0

	#print shared
	# Return
	return 1/(1+total)

#d = euclidDistance(critics,'Lisa Rose', 'Gene Seymour')
#print d
#-----------------------------------------------------------------------------------------------------------------------
''' Manhatten distance algorithm
	1) Identify the shared objects
	2) Calculate difference between the scores
	3) Sum the scores
	Minimum distance similar the people
	'''
def manhattan(itemData,ione,itwo):
	shared = {}
	total = 0
	for person in itemData[ione]:
		if person in itemData[itwo]:
			shared[person] = 1
			total += abs(itemData[ione][person] - itemData[itwo][person])

	if len(shared) == 0:
		return 0

	return 1/(1+total)
#-----------------------------------------------------------------------------------------------------------------------
# formula referred in http://onlinestatbook.com/2/describing_bivariate_data/calculation.html
def pearson(itemData,ione,itwo):
	shared = {}
	i1sum = i1sq = 0
	i2sum = i2sq = 0
	prodsum = 0
	for person in itemData[ione]:
		if person in itemData[itwo]:
			shared[person] = 1
			i1sum += itemData[ione][person]
			i1sq += itemData[ione][person]**2
			i2sum += itemData[itwo][person]
			i2sq += itemData[itwo][person]**2
			prodsum += itemData[ione][person]*itemData[itwo][person]

	length = len(shared)
	if length == 0:
		return 0

	numer = prodsum - ((i1sum*i2sum)/length)
	denom = ((i1sq-(i1sum**2/length))*(i2sq-(i2sum**2/length)))**0.5
	if denom == 0:
		return -1
	else:
		return numer/denom

#p = pearson(critics,'Lisa Rose', 'Gene Seymour')
#print p
#-----------------------------------------------------------------------------------------------------------------------
# http://www.statisticssolutions.com/correlation-pearson-kendall-spearman/


# A function to assign ranks and sort
#	the rankings
def spearman_sort(l):
	l = [[k,v] for k,v in l.items()]
	l.sort(key=lambda l:l[1])
	index = 1
	for each in l:
		each[1] = index
		index += 1
	l.sort()
	return l

''' Spearman Correlation algorithm
		1) Find scores of each object
		2) Calculate ranks for each object
		3) Find the difference between ranks,
			to verify - sum of ranks should be 0
		4) Calculate sum of squares of ranks
		5) Calculate Spearman r = 1 - (6*summ(d**2)/n(n**2-1)) '''
def spearman(itemData,ione,itwo):
	shared = {}

	# Find scores of each object
	x = {}
	y = {}
	index = 1
	for person in itemData[ione]:
		if person in itemData[itwo]:
			shared[person] = 1
			x[index] = itemData[ione][person]
			y[index] = itemData[itwo][person]
			index += 1

	# If no common element return 0
	l = len(shared)
	if l == 0:
		return -1

	# Calculate ranks for each object
	x = spearman_sort(x)
	y = spearman_sort(y)

	# Find the difference between ranks
	diff = []
	for index in range(0,len(x)):
		diff.append(x[index][1] - y[index][1])

	# Calculate sum of squares of ranks	
	diffs = 0
	for each in diff:
		diffs += each**2

	# Calculate Spearman r = 1 - (6*summ(d**2)/n(n**2-1))
	temp = (6*diffs)/(1+l*((l**2)-1))
	r = 1 - temp
	return r
#-----------------------------------------------------------------------------------------------------------------------
''' Cosine Similarity
	1) Find scores of each object
	2) Calculate ||x|| = sqrt(summ(x))
	3) Calculate ||y|| = sqrt(summ(y))
	4) Dot product x.y = summ(x*y)
	5) Cosine Similarity =  (x.y)/(||x||X||y||)
	'''
def cosine(itemData,ione,itwo):
	shared = {}
	dot = 0
	x = 0
	y = 0
	for person in itemData[ione]:
		if person in itemData[itwo]:
			shared[person] = 1
			x += itemData[ione][person]**2
			y += itemData[itwo][person]**2
			dot += itemData[ione][person]*itemData[itwo][person]

	if len(shared) == 0:
		return 0

	x = x**0.5
	y = y**0.5
	return dot/(x*y)
#-----------------------------------------------------------------------------------------------------------------------		
def tanimotoDistance(itemData, ione, itwo):
	num_in_both = 0

	for person in itemData[ione]:
		if person in itemData[itwo]:
			num_in_both += 1
	denom = len(itemData[ione]) + len(itemData[itwo]) - num_in_both

	if denom != 0:
		return float(num_in_both)/denom
	else:
		return 0
#-----------------------------------------------------------------------------------------------------------------------		
def minkowskiDistance(itemData, ione, itwo):
	shared = {}
	total = 0 
	r = 4
	for person in itemData[ione]:
		if person in itemData[itwo]:
			shared[person] = 1
			total += (itemData[ione][person]-itemData[itwo][person])**r

	if len(shared) == 0:
		return 0

	power = float(1)/r
	return total**power
#-----------------------------------------------------------------------------------------------------------------------		
'''def adjustedCosine(itemData, ione, itwo):
	userData = critics
	avg = {}
	for user in userData:
		sum_rating = 0
		count = 0
		for movie in userData[user]:
			sum_rating += userData[user][movie]
			count += 1 
		avg[user] = sum_rating/count
	sum_all = 0
	sum_first_sq = 0
	sum_second_sq = 0
	for user in userData:
		if (pone in user) and (ptwo in user):
			sum_first = (userData[user][pone] - avg[user]) 
			sum_second = (userData[user][ptwo] - avg[user])
			sum_num += sum_first * sum_second
			sum_first_sq += sum_first ** 2
			sum_second_sq += sum_second ** 2
	sum_den = (sum_first_sq * sum_second_sq )**0.5
	if sum_den != 0:
		return sum_num/sum_den
	else
		return 0
	'''