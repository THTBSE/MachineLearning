import numpy as np 
import pandas as pd 

def loadSimpleData():
	train_data = np.array([[1.0,2.1],[2.0,1.1],[1.3,1.0],[1.0,1.0],[2.0,1.0]])
	class_label = np.array([1.0,1.0,-1.0,-1.0,1.0])
	class_label = class_label.reshape((5,1))
	return train_data,class_label

class AdaBoost():
	def __init__(self,n_estimator = 20, epsilon = 0.1):
		self.n_estimator = n_estimator
		self.epsilon = epsilon
		self.D = None
		self.alphas = []
		self.stumps = []

	def stumpClassify(self,train_data,dim,threshval,flag):
		predictResult = np.ones((train_data.shape[0],1.0))
		if flag == 'lt':
			predictResult[train_data[0::,dim] <= threshval] = -1.0
		else:
			predictResult[train_data[0::,dim] > threshval] = -1.0
		return predictResult

	#D is the weight of each training example
	def buildDecisionStump(self,train_data,class_label,D):
		m,n = train_data.shape
		minError = np.inf
		numSteps = 10
		bestStump = {}
		predictGx = np.ones((m,1))
		for i in xrange(n):
			rangeMin = train_data[0::,i].min() 
			rangeMax = train_data[0::,i].max()
			stepLength = (rangeMax - rangeMin) / numSteps
			threshvals = [rangeMin + k * stepLength for k in range(numSteps+1)]
			for threshval in threshvals:
				for inequalflag in ['lt','gt']:
					predictResult = stumpClassify(train_data,i,threshval,inequalflag)
					errFlag = np.ones((m,1))
					errFlag[predictResult == class_label] = 0.0
					errWeight = np.dot(D.T,errFlag)

					print 'split:dim {0}, thresh {1}, thresh inequal: {2}, the weight error is :{3}'.format(i,\
						threshval,inequalflag,errWeight)
					if errWeight < minError:
						minError = errWeight
						predictGx = predictResult.copy()
						bestStump['dim'] = i
						bestStump['threshval'] = threshval
						bestStump['inequal'] = inequalflag

		return bestStump,minError,predictGx

	def predict(self,data):
		predictResult = []
		alphas = np.array(self.alphas)
		#predict by weak classifier
		for x in data:
			resultList = []
			for stump in self.stumps:
				dim = stump['dim']
				thresh = stump['threshval']
				result = 1.0
				if stump['inequal'] == 'lt':
					if x[dim] <= thresh:
						result = -1.0
				else:
					if x[dim] > thresh:
						result = -1.0
				resultList.append(result)
			resultList = np.array(resultList)
			prediction = np.dot(alphas.T,resultList)
			if prediction >= 0:
				predictResult.append(1.0)
			else:
				predictResult.append(-1.0)

		predictResult = np.array(predictResult)
		return predictResult
		
	def fit(self,train_data,class_label):
	 	train_data = np.array(train_data)
	 	m,n = train_data.shape
	 	class_label = np.array(class_label).reshape((m,1))
	 	self.D = np.ones((m,1)) / m
	 	for i in range(self.n_estimator):
	 		stump,errorRate,pGm = buildDecisionStump(train_data,class_label,self.D)
	 		alpha = 0.5 * np.log((1-errorRate)/errorRate)
	 		yDotGm = class_label * pGm
	 		ZmList = [w * np.exp(-alpha*yGm) for w,yGm in zip(self.D,yDotGm)]
	 		ZmList = np.array(ZmList)
	 		Zm = ZmList.sum()
	 		self.D = ZmList / Zm

	 		self.stumps.append(stump)
	 		self.alphas.append(alpha)

	 		predictLabel = predict(train_data)
	 		predictErrors = np.ones((m,1))
	 		predictErrors[predictLabel == class_label] = 0.0
	 		errorsRate = predictErrors.sum() / predictErrors.size

	 		print 'Epoch {0},Errors rate is :{1}'.format(i,errorsRate)
	 		if errorsRate < self.epsilon:
	 			break

