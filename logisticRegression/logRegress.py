import numpy as np 
import pandas as pd 
import math
import random

class LogisticRegression():
	def __init__(self,C,learning_rate,eta0,eplison,random_state=0,p=0.95,shuffle=True,max_iter=100):
		self.weights = None #w[0] is bias
		self.C = C
		self.learning_rate = learning_rate
		self.eta0 = eta0
		self.alpha = alpha
		self.max_iter = max_iter
		self.eplison = eplison
		self.p = p
		self.shuffle = shuffle
		self.rng = random.Random(random_state)
		self.E_grad_square = 0
		self.E_deltaw_square = 0

	def _sigmoid(self,z):
		return (1.0 / (1 + math.exp(-z)))

	def _rms(self,z,eps=1e-6):
		return math.sqrt(z+eps)

	def _adadelta(self,p,E_grad_square,E_deltaw_square,gradient):
		"""AdaDelta algorithm for calculating delta_w \
		where deltaa_w in formula:w[t+1] = w[t] + delta_w"""
		grad_square = sum([g*g for g in gradient])
		E_grad_square = p * E_grad_square + (1 - p) * grad_square
		coefficient = - self._rms(E_deltaw_square) / self._rms(E_grad_square) 
		delta_w = [coefficient * gi for gi in gradient]
		delta_w_square = sum([w*w for w in delta_w])
		E_deltaw_square = p * E_deltaw_square + (1 - p) * delta_w_square
		return delta_w,E_grad_square,E_deltaw_square 

	def _shuffle(self,X,y):
		shuffle_index = range(len(X))
		shuffle_index = self.rng.sample(shuffle_index,len(shuffle_index))
		X = [X[index] for index in shuffle_index]
		y = [y[index] for index in shuffle_index]
		return X,y

	def fit(self,X,y):
		dim = len(X[0])
		self.weights = [0 for i in range(dim+1)] #x0=1,w[0]=bias
		x0 = 1
		for i in range(self.max_iter):
			X,y = self._shuffle(X,y)
			for xi,yi in zip(X,y):
				xi = [1] + list(xi) #let x[0] = 1
				z = sum([wj * xij for wj,xij in zip(self.weights,xi)])
				pred = self._sigmoid(z)
				residual = pred - yi
				gradient = [residual * xij + self.C * wj for xij,wj in zip(xi,self.weights)]

				if self.learning_rate == 'adadelta':
					delta_w,self.E_grad_square,self.E_deltaw_square
					 = self._adadelta(self.p,self.E_grad_square,self.E_deltaw_square,gradient)
				else:
					delta_w = [-self.eta0*gj for gj in gradient]
					self.eta0 *= self.p

				self.weights = [wj+delta_wj for wj,delta_wj in zip(self.weights,delta_w)]


	def predict(self,dataSet):
		if not isinstance(dataSet,np.ndarray):
			dataSet = np.array(dataSet)

		z = np.dot(dataSet,self.weights[:-1]) + self.weights[-1]
		h0 = map(self.sigmoid,z)
		h0 = np.array(h0)
		h0[h0 >= 0.5] = 1
		h0[h0 < 0.5] = 0
		return h0

	#stochastic gradient ascend
	def sga(self,dataSet,label):
		m = dataSet.shape[0]
		for i in range(self.epoch):
			for x,y in zip(dataSet,label):
				yMinusH0 = y - self.sigmoid(np.dot(self.weights.T,x))
				deltaW = yMinusH0 * x
				self.weights = self.weights + self.alpha * deltaW

			predicts = self.predict(dataSet[:,:-1])
			errorRate = predicts[predicts != label].size / float(m)
			print 'epoch{0},error rate is:{1}'.format(i,errorRate)

	def fit(self,dataSet,label):
		df = pd.DataFrame(dataSet)
		df[df.columns[-1]+1] = np.ones((df.shape[0],1))

		if not isinstance(label,np.ndarray):
			label = np.array(label)

		self.weights = np.ones((df.shape[1],))
		self.sga(df.values,label)
		return self



def loadDataSet():
	dataSet = []
	label = [] 
	for line in open('testSet.txt','r'):
		line = map(float,line.rstrip().split('\t'))
		dataSet.append(line[:-1])
		label.append(line[-1])
	return dataSet,label

def plotFig(w,dataSet,label):
	import matplotlib.pyplot as plt 
	set1 = []
	set2 = []


	for x,y in zip(dataSet,label):
		if y == 1:
			set1.append(x)
		else:
			set2.append(x)

	set1 = np.array(set1)
	set2 = np.array(set2)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(set1[:,0],set1[:,1],s=30,c='r',marker='s')
	ax.scatter(set2[:,0],set2[:,1],s=30,c='g')

	x = np.arange(-3.0,3.0,0.1)
	y = (-w[2] - w[0]*x)/w[1]
	ax.plot(x,y)
	plt.xlabel('X1')
	plt.ylabel('X2')
	plt.show()


if __name__ == '__main__':
	dataSet,label = loadDataSet()
	clf = LogisticRegressor(80)
	clf = clf.fit(dataSet,label)
	print clf.weights
	plotFig(clf.weights,dataSet,label)