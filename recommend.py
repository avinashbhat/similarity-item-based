from engines import pearson, euclid, spearman, manhattan, cosine, tanimotoDistance, minkowskiDistance#, adjustedCosine
from data import loadData, critics, load1mData, load10mData, loadNewData
import math

# n is how many results you want 
# sim is the similarity function you want to use
# person is the person or movie whose similar one we need to find
# function to find similar user or movie, user - user prediction
# function returns a list of most similar items to the chosen item
def similar(itemData,item,e = 0,n=5):
	indices = { 0: euclid, 
				1: manhattan, 
				2: pearson, 
				3: spearman, 
				4: cosine,
				5: tanimotoDistance,
				6: minkowskiDistance }

	sim = indices[e]
	s = []
	for movie in itemData:
		#print movie
		if movie != item:
			s.append((sim(itemData,item,movie),movie))
	s.sort()
	s.reverse()
	# Return the best n results
	return s[0:n]



# This is a function to transform the data from user-item to item-user 
# Used for item based collaborative filtering

def transformData(data):
	result = {}
	for person in data : 
		for item in data[person]:
			#create nested dictionary for each item in the 'result' dictionary
			result.setdefault(item, {})
			result[item][person] = data[person][item] #flip the dataset
	return result


# This is a function used to calculate the similarity of items in a dataset
# sim denotes the similarity measure you want to use
# function returns a dictionary of lists of topMatches for items
def similarItems(dataset, itemData, e = 0, n=5):
	result = {}
	for item in itemData:
		result[item] = similar(itemData, item, e)
	return result


# This function is used to normalise a rating from range [1,5] to [-1, 1]
def Norm(val):
	normVal = (2*(val-1) - 4)/4
	return normVal


# This function is used to denormalise a rating from range [-1,1] to [1,5]
def Denorm(val):
	denormVal = ((val+1)*2) + 1
	return denormVal


# This function is used to recommend similar items to a given item for a particular user
# 'user' is the person to who recommendation is made
# simItem is the dictionary of similar items in dataset 
# returns list of tuples
def recommendItemsNorm(itemData, simItem, data):
	predicted = {}
	for user in data:
		for item in itemData:
			predicted.setdefault(user, {})
			num = 0
			den = 0
			for N in simItem[item]:
				if N[1] in data[user]:
					num += N[0]*Norm(data[user][N[1]])
					den += abs(N[0])
			if den != 0:
				val = Denorm(num/den)
			else:
				val = 0
			predicted[user][item] = val
	return predicted


# This function is used to predict the values for a given user in the test dataset
def slopeOne(itemData, simItem, data):
	cardinality = {}
	deviation = {}
	num = 0
	den = 0
	for user in data:
		for item1 in itemData:
			for item2 in itemData:
				deviation.setdefault(item1, {})
				cardinality.setdefault(item1, {})
				if item1 != item2:
					for user in data:
						if item1 in data[user] and item2 in data[user]:
							num += (data[user][item1]-data[user][item2])
							den += 1
			deviation[item1][item2] = num/den
			cardinality[item1][item2] = den
			num = den = 0
	
		prediction = {}
		for item1 in itemData:
			for item2 in simItem[item1]:
				num = 0
				den = 0
				if item1 != item2:
					prediction.setdefault(user, {})
					num += (deviation[item2][item1] + data[user][item1]) * cardinality[item2][item1]
					den += cardinality[item2][item1]
			prediction[user][item2] = num/den