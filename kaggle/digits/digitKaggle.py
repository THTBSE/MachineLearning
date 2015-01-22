from random import *
from sklearn.neighbors import KNeighborsClassifier
import os

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

def debugClassifier(filename, numOfNeigh):
	x,y = loadTrainData(filename)
	tx,ty = getTestDataFromTrain(x,y)
	neigh = KNeighborsClassifier(n_neighbors = 3)
	neigh.fit(x,y)
	print 'build KNN classifier done'
	errorCount = 0
	numOfTest = len(tx)
	for i in range(numOfTest):
		py = neigh.predict(tx[i])
		if py != ty[i]:
			errorCount += 1
	print 'the error rate is:', float(errorCount) / numOfTest
	return neigh

#build classifier of the whole train.csv 
def buildClassifier(filename, numOfNeigh):
	x,y = loadTrainData(filename)
	neigh = KNeighborsClassifier(n_neighbors = 3)
	neigh.fit(x,y)
	print 'build KNN classifier done'
	return neigh

#load test data of test.csv
def loadTestData(filename):
	x = []
	file = open(filename,'rb')
	file.readline()
	for line in file.readlines():
		string = line.split(',')
		x.append([float(n) for n in string])
	print 'load test data done'
	return x

def predictTestCase(classifier, x):
	numOfTest = len(x)
	print 'number of test cases:', numOfTest
	f = open('result','w')
	for i in range(numOfTest):
		y = classifier.predict(x[i])
		f.write(str(y))
		f.write('\n')
		percent = float(i) / numOfTest
		os.system('clear')
		print 'complete %', 100*percent
	f.close()





