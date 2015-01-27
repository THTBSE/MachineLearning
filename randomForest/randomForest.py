import math
from numpy import random

def loadTrainData(filename):
	f = open(filename,'r')
	f.readline()
	x = []
	y = []
	#for line in f.readlines():
	for i in range(1000):
		line = f.readline()
		s = line.split(',')
		y.append(int(s[0]))
		s = s[1:]
		x.append([int(n) for n in s])
	return x,y

def loadTestData(filename):
	f = open(filename,'r')
	f.readline()
	x = []
	#for line in f.readlines():
	for i in range(10):
		line = f.readline()
		line = line.split(',')
		x.append([int(n) for n in line])
	return x

def GiniOfD(y):
	numD = len(y)
	C = {}
	for Yi in y:
		if Yi in C:
			C[Yi] += 1
		else:
			C[Yi] = 1
	#print C
	sum = 0
	for k in C:
		p = float(C[k]) / numD
		p **= 2
		sum += p
	sum = 1 - sum
	#print 'Gini(D) is:',sum
	return sum

#A is a feature value
def GiniOfDA(x,y,A,index):
	y1 = []
	y2 = []
	numD = len(y)
	for i in range(numD):
		if x[i][index] == A:
			y1.append(y[i])
		else:
			y2.append(y[i])
	if not y1 or not y2:
		return 100000.0
	GiniD1 = GiniOfD(y1)
	GiniD2 = GiniOfD(y2)
	numD1 = len(y1)
	numD2 = len(y2)
	Gini = (float(numD1) / numD) * GiniD1 + (float(numD2) / numD) * GiniD2
	#print 'Gini(D,A) is:', Gini,'y1',y1,'y2',y2
	return Gini 

def minGiniOfAf(x,y,Af,index):
	minGini = 100000.0
	value = 0
	for A in Af: 
		Gini = GiniOfDA(x,y,A,index)
		if Gini < minGini:
			minGini = Gini
			value = A
	#print 'minGini:',minGini,' feature index:',index,' feature value:',value
	return minGini, value

def minGiniOfF(x,y,f,fi):
	minGini = 100000.0
	minIndex = -1
	minValue = 0
	stopFlag = False
	for i in fi:
		gini,value = minGiniOfAf(x,y,f[i],i)
		if gini < minGini:
			minGini = gini
			minIndex = i
			minValue = value
	if minGini > 10000:
		stopFlag = True
	#print 'mingini:',minGini,'minIndex',minIndex,'minValue',minValue,'len(fi)',len(fi)
	return minIndex,minValue,stopFlag

class node(object):
	def __init__(self):
		self.fIndex = None
		self.fValue = None
		self.left = None
		self.right = None
		self.label = None

class CARTree(object):
	def __init__(self):
		self.root = node()

def tellTheLabel(y):
	C = {}
	label = None
	for Yi in y:
		if Yi in C:
			C[Yi] += 1
		else:
			C[Yi] = 1
	maxY = -1
	for k in C:
		if C[k] > maxY:
			maxY = C[k]
			label = k
	return label

def buildOneNode(x,y,stopGini,root,f,fi):
	gini = GiniOfD(y)
	#print gini
	if gini < stopGini:
		root.label = tellTheLabel(y)
		return

	root.fIndex, root.fValue, stopFlag = minGiniOfF(x,y,f,fi)
	if stopFlag:
		root.label = tellTheLabel(y)
		return

	x1 = []
	y1 = []
	x2 = []
	y2 = []

	index = root.fIndex
	value = root.fValue
	fi.remove(index)
	if not fi:
		root.label = tellTheLabel(y)
		return
	for i,Xi in enumerate(x):
		if Xi[index] == value:
			x1.append(Xi)
			y1.append(y[i])
		else:
			x2.append(Xi)
			y2.append(y[i])
	root.left = node()
	root.right = node()
	buildOneNode(x1,y1,stopGini,root.left,f,fi)
	buildOneNode(x2,y2,stopGini,root.right,f,fi)
	return

def buildDecisionTree(x,y,stopGini,f,fi):
	numD = len(x)
	numF = len(x[0])
	f = [set([]) for i in range(numF)]
	for n in x:
		for i in range(numF):
			f[i].add(n[i])
	print f
	fi = range(numF)
	tree = node()
	buildOneNode(x,y,stopGini,tree,f,fi)
	return tree

def predict(tree,x):
	root = tree
	while root.label == None:
		if x[root.fIndex] == root.fValue:
			root = root.left
		else:
			root = root.right
	return root.label

def randomForest(x,y,numTrees,stopGini):
	numD = len(x)
	numF = len(x[0])
	f = [set([]) for i in range(numF)]
	for n in x:
		for i in range(numF):
			f[i].add(n[i])
	fValid = []
	for i,fn in enumerate(f):
		if len(fn) > 1:
			fValid.append(i)
	#print len(fValid)
	m = int(math.sqrt(len(fValid)))
	forest = []
	for i in range(numTrees):
		sampleX = []
		sampleY = []
		for j in range(numD):
			index = random.random_integers(0,numD-1)
			sampleX.append(x[index])
			sampleY.append(y[index])
		allf = fValid[:]
		fi = []
		for j in range(m):
			index = random.randint(0,len(allf)-1)
			fi.append(allf[index])
			del allf[index]
		tree = node()
		buildOneNode(sampleX,sampleY,stopGini,tree,f,fi)
		forest.append(tree)
		print 'train ',i,'tree'
	return forest

def rfPredict(forest,x):
	labelCount = {}
	for tree in forest:
		y = predict(tree,x)
		if y in labelCount:
			labelCount[y] += 1
		else:
			labelCount[y] = 1
	label = -1
	maxNum = -1
	for y in labelCount:
		if labelCount[y] > maxNum:
			maxNum = labelCount[y]
			label = y
	return label

x,y = loadTrainData('train.csv')
#tree = buildDecisionTree(x,y,0.2)
n = raw_input('Please input the number of trees you need:')
n = int(n)

forest = randomForest(x,y,n,0.1)
xTest = loadTestData('test.csv')

#for i,Xi in enumerate(x):
#	Yi = predict(tree,Xi)
#	if Yi == y[i]:
#		print 'correct',i,' yi',Yi
#	else:
#		print 'error',i

for Xi in xTest:
	yi = rfPredict(forest,Xi)
	print yi

	