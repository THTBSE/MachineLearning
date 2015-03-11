import numpy as np 
import random
import matplotlib.pyplot as plt 

def loadDataSet(filename):
	result = []
	for line in open(filename,'rb'):
		line = line.rstrip().split('\t')
		num = [float(x) for x in line]
		result.append(num)
	result = np.array(result)
	return result

class kMeans():
	def __init__(self, k = 2):
		self.k = k 
		self.cluster_centers = []

	def __updateCenter(self,X,cluster):
		for i,group in enumerate(cluster):
			print group
			print '--------------------'
			X_ = [X[index] for index in group]
			print self.cluster_centers[i]
			self.cluster_centers[i] = reduce(lambda x,y:x+y,X_) * (1.0 / len(group))
			print self.cluster_centers[i]
			print '!!!!!!!!!!!!!!!!!!!!!!'
		print '***************'
	def __initialize(self,X):
		cluster = [set([]) for i in range(self.k)]
		rd = random.Random()
		self.cluster_centers = rd.sample(X,self.k)
		for i,m in enumerate(X):
			dist = [np.linalg.norm(m-center) for center in self.cluster_centers]
			index = dist.index(min(dist))
			cluster[index].add(i)
		self.__updateCenter(X,cluster)
		return cluster

	def fit(self,X):
		cluster = self.__initialize(X)
		changed = True
		epoch = 0
		maxEpoch = 50
		while changed:
			changed = False
			Ncluster = [set([]) for i in range(self.k)]
			for i,m in enumerate(X):
				dist = [np.linalg.norm(m-center) for center in self.cluster_centers]
				index = dist.index(min(dist))
				Ncluster[index].add(i)
			if True in map(lambda x,y:x != y,Ncluster,cluster):
				cluster = Ncluster
				self.__updateCenter(X,cluster)
				changed = True
			elif epoch == maxEpoch:
				break
			epoch = epoch + 1
			print 'epoch {0}'.format(epoch)
		return cluster

data = loadDataSet('testSet.txt')
clf = kMeans(4)
clr = ['r','g','b','r']
cluster = clf.fit(data)
for c,clr in zip(cluster,clr):
	X = [data[index] for index in c]
	X = np.array(X)
	plt.scatter(x=X[:,0],y=X[:,1],c=clr,marker='s',s=90)
plt.show()

