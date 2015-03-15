import numpy as np 

class RandomForestRegressor():
	def __init__(self,n_estimators=50,tolS=1,tolN=4):
		self.n_estimators = n_estimators
		self.tolS = tolS
		self.tolN = tolN
		self.Forest = []

	def __BinarySplit(self,data,dim,val):
		subData1 = data[data[:,dim] > val]
		subData2 = data[data[:,dim] <= val]
		return subData1,subData2

	def __regErrors(self,data):
		return np.var(data[:,-1]) * data.shape[0]

	def __LeafValue(self,data):
		return data[:,-1].mean()

	def __BestSplit(self,data,regErrors=__regErrors,leafType=__LeafValue):
		currLeafValue = self.__LeafValue(data)
		if len(set(data[:,-1])) == 1:
			return None,currLeafValue
		currErrors = self.__regErrors(data)
		m,n = data.shape
		minErrors = np.inf
		dim = None
		val = currLeafValue
		for i in range(n-1):
			for featureVals in set(data[:,i]):
				subData1,subData2 = self.__BinarySplit(data,i,featureVals)
				if subData1.shape[0] < self.tolN or subData2.shape[0] < self.tolN:
					continue
				Errors = self.__regErrors(subData1) + self.__regErrors(subData2)
				if Errors < minErrors:
					minErrors = Errors
					dim = i
					val = featureVals
		if (currErrors - minErrors) < self.tolS:
			return None,currLeafValue
		return dim,val

	def __CreateTree(self,data):
		dim,val = self.__BestSplit(data)
		if dim == None:
			return val
		regTree = {}
		regTree['dim'] = dim
		regTree['val'] = val 
		subData1,subData2 = self.__BinarySplit(data,dim,val)
		regTree['left'] = self.__CreateTree(subData1) 
		regTree['right'] = self.__CreateTree(subData2)
		return regTree

	def __TreePredict(self,tree,x):
		while True:
			if isinstance(tree,dict):
				SplitDim = tree['dim']
				SplitVal = tree['val']
				if x[SplitDim] > SplitVal:
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
		return np.mean(predicts)

	def fit(self,train_data,values):
		if isinstance(train_data,list):
			train_data = np.array(train_data)
		if isinstance(values,list):
			values = np.array(values)

		#merge x,y to one matrix
		m,n = train_data.shape
		data = np.ones((m,n+1))
		if n == 1:
			data[:,0] = train_data[:,0]
		else: 
			data[:,0:-1] = train_data
		data[:,-1] = values

		for i in xrange(self.n_estimators):
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

