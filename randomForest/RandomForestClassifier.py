import numpy as np 

__author__ = 'Frank'

class RandomForest():
	def __init__(self,n_estimator=50,tolS=0.1,tolN=4):
		self.n_estimator = n_estimator
		self.tolS = tolS
		self.tolN = tolN
		self.Forest = []
	
	def __BinarySplit(self,data,dim,val):
		subData1 = data[data[:,dim] == val]
		subData2 = data[data[:,dim] != val]
		return subData1,subData2

	def __LeafValue(self,data):
		return np.bincount(map(int,data[:,-1])).argmax()

	def __GiniOfSet(self,data):
		totalSize = data.shape[0]
		classStat = np.bincount(map(int,data[:,-1]))
		classStat = [(float(x) / totalSize) ** 2 for x in classStat]
		Gini = 1 - sum(classStat)
		return Gini

	def __BestSplit(self,data):
		currLeafVal = self.__LeafValue(data)
		if len(np.unique(data[:,-1])) == 1:
			return None,currLeafVal 

		currGini = self.__GiniOfSet(data)
		if currGini < self.tolS:
			return None,currLeafVal

		m,n = data.shape
		m = float(m)
		minGini = np.inf
		val = currLeafVal
		dim = None
		for i in range(n-1):
			for featureVal in np.unique(data[:,i]):
				subData1,subData2 = self.__BinarySplit(data,i,featureVal)
				if subData1.shape[0] < self.tolN or subData2.shape[0] < self.tolN:
					continue
				Gini = (subData1.shape[0]/m) * self.__GiniOfSet(subData1) + (subData2.shape[0]/m) * self.__GiniOfSet(subData2)
				if Gini < minGini:
					minGini = Gini
					val = featureVal
					dim = i
		return dim,val

	def __CreateTree(self,data):
		dim,val = self.__BestSplit(data)
		#when dim == None, the val is the leaf node which predicts the class type
		if dim == None:
			return val
		ClassifyTree = {}
		ClassifyTree['dim'] = dim
		ClassifyTree['val'] = val
		subData1,subData2 = self.__BinarySplit(data,dim,val)
		ClassifyTree['left'] = self.__CreateTree(subData1)
		ClassifyTree['right'] = self.__CreateTree(subData2)
		return ClassifyTree

	def __TreePredict(self,tree,x):
		while True:
			if isinstance(tree,dict):
				SplitDim = tree['dim']
				SplitVal = tree['val']
				if x[SplitDim] == SplitVal:
					tree = tree['left']
				else:
					tree = tree['right']
			else:
				return tree

	def __ForestPredict(self,x):
		predicts = []
		for tree in self.Forest:
			pResult = self.__TreePredict(tree,x)
			predicts.append(pResult)
		return np.bincount(predicts).argmax()

	def fit(self,train_data,labels):
		if isinstance(train_data,list):
			train_data = np.array(train_data)
		if isinstance(labels,list):
			labels = np.array(labels)

		#merge x,y to one matrix
		m,n = train_data.shape
		data = np.ones((m,n+1))
		if n == 1:
			data[:,0] = train_data[:,0]
		else: 
			data[:,0:-1] = train_data
		data[:,-1] = labels

		for i in xrange(self.n_estimator):
			randSet = []
			for j in xrange(m):
				rIndex = np.random.randint(0,m)
				randSet.append(data[rIndex])
			randSet = np.array(randSet)
			CARTree = self.__CreateTree(randSet)
			self.Forest.append(CARTree)
			print '{0} tree has been created'.format(i)
		return self

	def predict(self,data):
		predicts = map(self.__ForestPredict,data)
		return predicts