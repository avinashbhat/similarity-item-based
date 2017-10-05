from recommend import similar, transformData, similarItems, recommendItemsNorm, slopeOne
from data import loadData, critics, loadNewData
from engines import euclid, spearman, manhattan, pearson, cosine, tanimotoDistance, minkowskiDistance#, adjustedCosine
import itertools
import time


#load the data set
dataset = loadData()
#dataset = critics
itemData = transformData(dataset)
#print itemData

# A function to spilt the data to training and test sets
def splitDict(d):
    n = int(len(d) * 0.85)         
    i = d.iteritems()
    d1 = dict(itertools.islice(i, n))  
    d2 = dict(i)                        
    return d1, d2

#trainingData, testData = splitDict(dataset)
#training, test = splitDict(dataset)

# A function to calculate MAE
def mae(ordered, test):
	isum = 0
	tot_sum = 0
	num = 0
	tot_num = 0
	for each in ordered:
		tot_num += 1
		for movie in ordered[each]:
			if movie in test[each]:
				num += 1
				error = test[each][movie] - ordered[each][movie]
				if error < 0:
					error = 0 - error
				isum = isum + error
		tot_sum += isum/num
		num = 0
		isum = 0
	return tot_sum/tot_num

# A function to calculate RMSE
def rmse(ordered, test):
	isum = 0
	tot_sum = 0
	num = 0
	tot_num = 0
	for each in ordered:
		tot_num += 1
		for movie in ordered[each]:
			if movie in test[each]:
				num += 1
				error = (test[each][movie] - ordered[each][movie])**2
				isum = isum + error
		tot_sum += (isum)**0.5/num
		num = 0
		isum = 0
	return tot_sum/tot_num

# A driver function to calculate the time taken for each recommendation and also the 
# error in each calculation
# dataset is the entire data
# itemData is the modified dataset
def driver(i):
	predictedNorm = {}
	predictedSlope = {}
	start = time.clock()
	simItem = similarItems(dataset, itemData, i)
	end = time.clock()
	# Time taken for calculating the similarity
	# print end - start

	predictedNorm = recommendItemsNorm(itemData, simItem, dataset)

for i in range(0, 1):
	driver(i)