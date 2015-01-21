from random import *
from sklearn.neighbors import KNeighborsClassifier

def loadTrainData(filename):
	file = open(filename,'rb')
	x = []
	y = []
	file.readline()
	for line in file.readlines():
		#line = file.readline()
		string = line.split(',')
		y.append(int(string[0]))
		s1 = string[1:]
		Xi = [float(n) for n in s1]
		x.append(Xi)
	print 'loadData done'
	return x, y

def getTestDataFromTrain(x, y):
	tx = []
	ty = []
	numOfInput = len(x)
	numOfTest = int(0.1 * numOfInput)
	while numOfTest > 0:
		index = int(numOfInput * random())
		tx.append(x[index])
		ty.append(y[index])
		x.pop(index)
		y.pop(index)
		numOfTest -= 1
		numOfInput -= 1
	print 'getTestData done'
	return tx, ty

def digitClassify(filename, numOfNeigh):
	x,y = loadTrainData(filename)
	tx,ty = getTestDataFromTrain(x,y)
	neigh = KNeighborsClassifier(n_neighbors = 3)
	neigh.fit(x,y)
	print 'KNN done'
	errorCount = 0
	numOfTest = len(tx)
	for i in range(numOfTest):
		py = neigh.predict(tx[i])
		if py != ty[i]:
			errorCount += 1
	print 'the error rate is:', float(errorCount) / numOfTest
	return neigh





