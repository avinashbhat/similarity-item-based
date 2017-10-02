from engines import pearson, euclid, spearman, manhattan, cosine, tanimotoDistance, minkowskiDistance#, adjustedCosine
from data import loadData, critics

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
		#print item
		result[item] = similar(itemData, item, e)
	return result


# This function is used to recommend similar items to a given item for a particular user
# 'user' is the person to who recommendation is made
# simItem is the dictionary of similar items in dataset 
# returns list of tuples
def recommendItems(data, simItem, user, n):
	userRatings = {}
	userRatings = data[user]
	scores = {}
	totalSim = {}

	rankings = []

	for (item, rating) in userRatings.items() :
		for (similarity, item2) in simItem[item] :
			if item2 in userRatings : continue
			scores.setdefault(item2, 0)
			scores[item2] += similarity * rating

			totalSim.setdefault(item2, 0)
			totalSim[item2] += similarity

	for (item, score) in scores.items() :
		rankings.append((score/totalSim[item], item))

	rankings.sort()
	rankings.reverse()
	return rankings[0:n]