import numpy as np 
import csv


class recommender():
	def __init__(self,data,metric = 'minkowski',k = 3,reN = 1):
		self.n = reN
		self.k = k
		self.data = data
		self.metric = metric
		if self.metric == 'minkowski':
			self.simDistance = self.simMinkowski
		elif self.metric == 'pearson':
			self.simDistance = self.simPearson

	def simPearson(self,rating1,rating2,r = None):
		sumX = 0.0
		sumY = 0.0
		XDotY = 0.0
		sumXSqr = 0.0
		sumYSqr = 0.0
		n = 0
		for item in rating1:
			if item in rating2:
				n += 1
				x = rating1[item]
				y = rating2[item]
				sumX += x
				sumY += y
				XDotY += x * y
				sumXSqr += x ** 2
				sumYSqr += y ** 2

		denominator = np.sqrt(sumXSqr - (sumX**2)/n) * np.sqrt(sumYSqr - (sumY**2)/n)
		if denominator == 0:
			return 0
		r = (XDotY - (sumX*sumY)/n) / denominator
		return r

	def simMinkowski(self,rating1,rating2,r = 2):
		sumPowX_Y = 0.0
		r_1 = 1.0 / r
		distList = [abs(rating1[item]-rating2[item])**r for item in rating1 if item in rating2]
		distance = np.inf
		if distList:
			distance = pow(sum(distList),r_1)
		return distance

	def findSimilarity(self,userName):
		neighbors = []
		for other in self.data:
			if userName != other:
				distance = self.simDistance(self.data[userName],self.data[other])
				neighbors.append((distance,other))
		neighbors.sort(key=lambda x:x[0])
		if self.metric == 'pearson':
			neighbors.reverse()

		return neighbors[:self.k]

	def recommendation(self,userName):
		neighbors = self.findSimilarity(userName)
		coeffSum = reduce(lambda x,y:x+y[0],neighbors,0.0)
		weights = [dist[0] / coeffSum for dist in neighbors]
		if self.metric == 'minkowski':
			weights.reverse()

		recomend = {}
		for i in range(len(neighbors)):
			otherName = neighbors[i][1]
			for item in self.data[otherName]:
				if not item in self.data[userName]:
					if not item in recomend:
						recomend[item] = self.data[otherName][item] * weights[i]
					else:
						recomend[item] += self.data[otherName][item] * weights[i]
		recomend = recomend.items()
		recomend.sort(key=lambda x:x[1],reverse=True)
		return recomend[:3]


def loadDataSet(filename):
	f = open(filename,'r')
	csv_reader = csv.reader(f)
	header = csv_reader.next()
	header = header[1:]
	data = {}
	for user in header:
		data[user] = {}
	userCount = len(header)
	for row in csv_reader:
		moive = row[0]
		row = row[1:]
		for i in range(userCount):
			if row[i]:
				user = header[i]
				data[user][moive] = float(row[i])
	return data 


if __name__ == '__main__':
	dataSet = loadDataSet('Movie_Ratings.csv')
	r = recommender(dataSet,metric='pearson',k=2,reN = 3)
	rec = r.recommendation('Heather')
	for x in rec:
		print x
