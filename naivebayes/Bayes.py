import pandas as pd 
import numpy as np 

class NaiveBayes():
	def __init__(self):
		self.py = None
		self.pxy = None
		self.labels = []

	def train(self,df):
		py = {}
		pxy = {}

		totalSize = float(df.shape[0])
		labels = list(set(df['label']))
		for y in labels:
			sub_df = df[df['label'] == y]
			size = sub_df.shape[0]
			p = size / totalSize
			py[y] = p 

		#for Laplace smoothing
		lamda = 1.0

		for y in labels:
			pxy[y] = {}
			ySize = float(df[df['label'] == y].shape[0])
			featN = df.columns.size - 1
			for n in range(featN):
				pxy[y][n] = {}
				features = set(df[n])
				Sj = len(features)
				for xj in features:
					size = df[(df[n] == xj) & (df['label'] == y)].shape[0]
					p = (size + lamda) / (ySize + Sj*lamda)
					pxy[y][n][xj] = p 

		return py,pxy,labels

	def fit(self,dataSet,label):
		df = pd.DataFrame(dataSet)
		df['label'] = label

		self.py,self.pxy,self.labels = self.train(df)

		return self

	def predict(self,testSet):
		results = []

		for X in testSet:
			plist = []
			for y in self.labels:
				p = self.py[y]
				for n in range(len(X)):
					p *= self.pxy[y][n][X[n]]
				plist.append(p)

			#print plist
			predictY = self.labels[np.argmax(plist)]
			results.append(predictY)

		return results

if __name__ == '__main__':
	dataSet = [[1,'S'],[1,'M'],[1,'M'],[1,'S'],[1,'S'],[2,'S'],[2,'M'],[2,'M'],[2,'L'],[2,'L'],[3,'L'],[3,'M']\
	,[3,'M'],[3,'L'],[3,'L']]

	labels = [-1,-1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1]

	print dataSet
	print '------'

	clf = NaiveBayes()
	clf = clf.fit(dataSet,labels)

	r = clf.predict([[2,'S']])

	print 'Predict result:{0}'.format(r)

	print '-----'
	for y in clf.pxy:
		for n in clf.pxy[y]:
			for xj in clf.pxy[y][n]:
				print 'p(X({0})={1}|Y={2}) = {3}'.format(n,xj,y,clf.pxy[y][n][xj])



			


