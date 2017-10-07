from recommend import similar, transformData, similarItems, recommendItemsNorm, slopeOne
from data import loadData, critics, loadNewData, load1mData, load10mData
from engines import euclid, spearman, manhattan, pearson, cosine, tanimotoDistance, minkowskiDistance#, adjustedCosine
import itertools
import time


#load the data set
#dataset = loadData()
#dataset = critics
#dataset = load1mData()
#dataset = load10mData()
dataset = loadNewData()
#print itemData

# A function to spilt the data to training and test sets
def splitDict(d):
    n = int(len(d) * 0.85)         
    i = d.iteritems()
    d1 = dict(itertools.islice(i, n))  
    d2 = dict(i)                        
    return d1, d2

training, test = splitDict(dataset)
itemData = transformData(training)

# A function to calculate MAE
def mae(predicted, test):
	isum = 0
	tot_sum = 0
	num = 0
	tot_num = 0
	# For each user in the test set,
	for user in test:
		# If we have predicted the possible movie ratings for that user
		if user in predicted:
			# For each movie user has actually rated
			for movie in test[user]:
				# If we have predicted the movie ratings
				if movie in predicted[user]:
					# Calculate the error between the ratings and count
					# number of such movies
					num += 1
					#print predicted[user][movie], " - ", test[user][movie]
					error = abs(predicted[user][movie] - test[user][movie])
					# Calculate the total possible error
					isum = isum + error
			# Calculate average error per movie and total it
			if not num == 0:
				tot_sum += isum/num
			# Count number of such users
			tot_num += 1
			num = 0
			isum = 0
	# Calculate Average error in the entire matrix
	return tot_sum/tot_num

# A function to calculate RMSE
def rmse(predicted, test):
	isum = 0
	tot_sum = 0
	num = 0
	tot_num = 0
	# For each user in the test set,
	for user in test:
		# If we have predicted the possible movie ratings for that user
		if user in predicted:
			# For each movie user has actually rated
			for movie in test[user]:
				# If we have predicted the movie ratings
				if movie in predicted[user]:
					# Calculate the error between the ratings, square it
					# and count number of such movies
					num += 1
					#print predicted[user][movie], " - ", test[user][movie]
					error = (predicted[user][movie] - test[user][movie])**2
					#print error
					# Calculate the total possible error
					isum = isum + error
			# Calculate average error per movie, root it and total it
			if not num == 0:
				tot_sum += (isum/num)**0.5
			# Count number of such users
			tot_num += 1
			num = 0
			isum = 0
	# Calculate Average error in the entire matrix
	return tot_sum/tot_num

# A driver function to calculate the time taken for each recommendation and also the 
# error in each calculation
# dataset is the entire data
# itemData is the modified dataset
def driver(i):
	predictedNorm = {}
	predictedSlope = {}
	start = time.clock()
	#simItem = similarItems(dataset, itemData, i)
	simItem = similarItems(training, itemData, i)

	end = time.clock()
	# Time taken for calculating the similarity
	print end - start

	#predictedNorm = recommendItemsNorm(itemData, simItem, dataset)
	adjusted = {}
	start = time.clock()
	predictedNorm = recommendItemsNorm(itemData, simItem, dataset)
	end = time.clock()
	print end - start
	for person in predictedNorm:
		adjusted.setdefault(person, {})
		for movie in predictedNorm[person]:
			if predictedNorm[person][movie] > 0:
				adjusted[person][movie] = predictedNorm[person][movie]
	#print predictedNorm
#	predictedSlope = slopeOne(itemData, simItem, dataset)

	'''ordered = {}
	for each in predicted:
		ordered.setdefault(each,{})
		for movie in predicted[each]:
			ordered[each][movie[1]] = movie[0]'''
	mae_error = mae(adjusted, test)
	print mae_error
	rmse_error = rmse(adjusted, test)
	print rmse_error
	print '---'

for i in range(0, 7):
	driver(i)