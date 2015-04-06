import pandas as pd
import numpy as np  
from sklearn.ensemble import RandomForestClassifier


def loadDataSet(filename):
	df = pd.read_csv(filename,header=0)
	return df

def hasStraight(x):
	cards = x.copy()
	cards.sort()
	for i in range(len(cards) - 1):
		if (cards[i]+1) != cards[i+1]:
			return 0
	return 1

def howMuchPairs(x):
	count = {}
	for n in x:
		count.setdefault(n,0)
		count[n] += 1
	return count.values().count(2)

def hasThree(x):
	count = {}
	for n in x:
		count.setdefault(n,0)
		count[n] += 1
	if 3 in count.values():
		return 1
	else:
		return 0

def hasFour(x):
	count = {}
	for n in x:
		count.setdefault(n,0)
		count[n] += 1
	if 4 in count.values():
		return 1
	else:
		return 0

def featureEngineering(df):
	card = df[['C1','C2','C3','C4','C5']].values
	color = df[['S1','S2','S3','S4','S5']].values

	#has flush?
	df['flush'] = map(lambda x:1 if len(set(x)) == 1 else 0,color)
	#has straight?
	df['straight'] = map(hasStraight,card)
	#has four of a kind?
	df['four'] = map(hasFour,card)
	#has three of a kind?
	df['three'] = map(hasThree,card)
	#how much pairs?
	df['pairs'] = map(howMuchPairs,card)
	return df 

def getLabels():
	return ['flush','straight','four','three','pairs']

if __name__ == '__main__':
	df = loadDataSet('train.csv')
	df = featureEngineering(df)
	print 'TrainData Feature Engineering Done!'
	clf = RandomForestClassifier(n_estimators = 200)
	labels = getLabels()
	clf = clf.fit(df.loc[:,labels],df.loc[:,'hand'])
	print 'Training... Done!'
	test = loadDataSet('test.csv')
	test = featureEngineering(test)
	print 'TestData Feature Engineering Done!'
	results = clf.predict(test.loc[:,labels])
	f = open('result.csv','w')
	f.write('id,hand\n')

	test_id = test.loc[:,'id']
	for index,hand in zip(test_id,results):
		f.write('{0},{1}\n'.format(index,hand))
	f.close()

