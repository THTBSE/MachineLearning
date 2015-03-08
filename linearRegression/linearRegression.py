import numpy as np 

def loadTrainData():
	f = open('abalone.txt','rb')
	train_data = []
	values = []
	for line in f:
		line = line.strip().split('\t')
		line = [float(x) for x in line]
		train_data.append(line[:-1])
		values.append(line[-1])
	train_data = np.array(train_data)
	values = np.array(values)
	return train_data,values

class LinearRegression():
	def __init__(self,alpha = 0.1,epochs = 40):
		self.weights = None
		self.bias = 1.0
		self.alpha = alpha
		self.epochs = epochs

	def error(self,predict,y):
		return ((predict - y) ** 2).sum()

	def predict(self,test_data):
		result = np.dot(test_data,self.weights) + self.bias
		return result

	def __SGD(self,train_data,values):
		"""
		stochastic gradient descent
		"""
		for i in xrange(self.epochs):
			for x,y in zip(train_data,values):
				error = np.dot(self.weights.T,x) + self.bias - y
				nabla_b = error
				nabla_w = error * x

				self.weights = self.weights - self.alpha * nabla_w
				self.bias = self.bias - self.alpha * nabla_b

			predictResult = self.predict(train_data)
			diff = ((values - predictResult) ** 2).sum()
			print 'epoch {0}, diff is :{1}'.format(i,diff)
		print self.weights
		print self.bias

	def fit(self,train_data,values):
		#convert list objects to numpy array
		train_data = np.array(train_data)
		m,n = train_data.shape
		values = np.array(values)

		self.weights = np.random.randn(n,)
		self.__SGD(train_data,values)


train_data,y = loadTrainData()
lr = LinearRegression()
lr.fit(train_data,y)

py = lr.predict(train_data[0:10])
print py
print y[0:10]
error = lr.error(py,y[0:10])
print error