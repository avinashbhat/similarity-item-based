critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

# A function to load the 100k dataset.
def loadData(path = '/home/avinash/Desktop/item/ml-100k/'):
	fhandle = open(path+'u.item')
	movies = {}
	for line in fhandle:
		(i,t) = line.split('|')[0:2]
		movies[i] = t
	data = {}
	fhandle = open(path+'u.data')
	for line in fhandle:
		(user, i, rating, t) = line.split('\t')
		data.setdefault(user, {})
		data[user][movies[i]] = float(rating)
	return data

# A function to check if the value is in a valid data format
def isFloat(num):
	try:
		float(num)
		return True
	except ValueError:
		return False


# A function to load recent datasets. (Here, ml-latest-small and ml-latest )
def loadNewData(path = 'ml-latest-small/'):
	fhandle = open(path+'movies.csv')
	movies = {}
	for line in fhandle:
		(i,t) = line.split(',')[0:2]
		movies[i] = t
	data = {}
	fhandle = open(path+'ratings.csv')
	for line in fhandle:
		(user,i,rating,t) = line.split(',')
		data.setdefault(user, {})
		if isFloat(rating):
			data[user][movies[i]] = float(rating)
		else:
			continue
	return data