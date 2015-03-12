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
		for i in range(self.k):
			self.cluster_centers[i] = X[cluster[:,0] == i].mean(axis = 0)

	def __initialize(self,X):
		cluster = np.zeros((X.shape[0],2))
		rd = random.Random()
		cluster_centers = rd.sample(X,2)
		for i,m in enumerate(X):
			dist = [((m - center) ** 2).sum() for center in cluster_centers]
			minDist = min(dist)
			index = dist.index(minDist)
			cluster[i,0] = index
			cluster[i,1] = minDist
		for i in range(2):
			cluster_centers[i] = X[cluster[:,0] == i].mean(axis = 0)
		return cluster,cluster_centers

	def fit(self,X):
		centroid = X.mean(axis = 0)
		self.cluster_centers = [centroid]
		cluster = np.zeros((X.shape[0],2))
		while len(self.cluster_centers) < self.k:
			SSE = [cluster[cluster[:,0] == i,1].sum() for i in range(len(self.cluster_centers))]
			index = SSE.index(max(SSE))
			bestCluster,cluster_centers = self.__binKmeans(X[cluster[:,0] == index])
			#index of bestCluster are 0,1! so we have to convert it , 0 to index, 1 to number of centers
			if index == 1:
				bestCluster[bestCluster[:,0] == 0,0] = len(self.cluster_centers)
			else:
				bestCluster[bestCluster[:,0] == 0,0] = index 
				bestCluster[bestCluster[:,0] == 1,0] = len(self.cluster_centers)
			self.cluster_centers[index] = cluster_centers[0]
			self.cluster_centers.append(cluster_centers[1])
			cluster[cluster[:,0] == index] = bestCluster
		return cluster

	def __binKmeans(self,X):
		cluster,cluster_centers = self.__initialize(X)
		changed = True
		while changed:
			changed = False
			for i,m in enumerate(X):
				dist = [np.linalg.norm(m-center) for center in cluster_centers]
				minDist = min(dist)
				index = dist.index(minDist)
				if cluster[i,0] != index:
					cluster[i,0] = index
					cluster[i,1] = minDist
					changed = True
			if changed:
				for i in range(2):
					cluster_centers[i] = X[cluster[:,0] == i].mean(axis = 0)
		return cluster,cluster_centers

data = loadDataSet('testSet2.txt')
clf = kMeans(3)
clr = [['r','^'],['g','s'],['b','o']]
cluster = clf.fit(data)
print clf.cluster_centers
for cr,i in zip(clr,range(clf.k)):
	X = data[cluster[:,0] == i]
	plt.scatter(x=X[:,0],y=X[:,1],c=cr[0],marker=cr[1],s=80)

clf.cluster_centers = np.array(clf.cluster_centers)
plt.scatter(x=clf.cluster_centers[:,0],y=clf.cluster_centers[:,1],marker='+',s=200)
plt.show()

