import numpy as np 
import pandas as pd 

class LogisticRegressor():
	def __init__(self,maxEpoch = 100, alpha = 0.1):
		self.weights = None
		self.alpha = alpha
		self.epoch = maxEpoch

	def sigmoid(self,z):
		return (1.0 / (1 + np.exp(-z)))

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