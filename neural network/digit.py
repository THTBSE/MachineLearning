import numpy as np 
from ann import *
import pickle

def loadTrainingData(filename):
	"""load the image data"""
	f = open(filename,'r')
	f.readline()
	tx = []
	ty = []
	for line in f.readlines():
		line = line.split(',')
		y = np.zeros((10,1))
		y[int(line[0])] = 1.0
		ty.append(y)
		line = line[1:]
		x = [int(n) / 255.0 for n in line]
		tx.append(np.ndarray(shape=(784,1),buffer=np.array(x)))
	f.close()
	print 'load training data done'
	return zip(tx,ty)

def loadTestDataFromTrain(training_data, cnt):
	test_data = []
	for i in xrange(0, cnt):
		index = np.random.randint(0,len(training_data))
		test_data.append(training_data[index])
		del training_data[index]
	print 'load test data done'
	return test_data

training_data = loadTrainingData('train.csv')
test_data = loadTestDataFromTrain(training_data, 1000)

network = ann([784,30,10])
network.SGD(training_data, 30, 10, 3.0, test_data = test_data)

train_result = open('train_result.txt','w')
pickle.dump(network,train_result)
train_result.close()



