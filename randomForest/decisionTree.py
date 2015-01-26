def loadTrainData(filename):
	f = open(filename,'r')
	f.readline()
	x = []
	y = []
	for line in f.readlines():
		s = line.split(',')
		y.append(int(s[0]))
		s = s[1:]
		x.append([int(n) for n in s])
	print x,y
	return x,y

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
	GiniD1 = GiniOfD(y1)
	GiniD2 = GiniOfD(y2)
	numD1 = len(y1)
	numD2 = len(y2)
	Gini = (float(numD1) / numD) * GiniD1 + (float(numD2) / numD) * GiniD2
	#print 'Gini(D,A) is:', Gini
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
	Gini = []
	Value = []
	for i in fi:
		gini,value = minGiniOfAf(x,y,f[i],i)
		Gini.append(gini)
		Value.append(value)
	minG = min(Gini)
	minIndex = Gini.index(minG)
	print 'min Gini:',minG,'minIndex',minIndex,'minValue',Value[minIndex]
	return minIndex, Value[minIndex]

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

def buildOneNode(x,y,stopGini,root,f,fi):
	gini = GiniOfD(y)
	print gini
	if gini < stopGini:
		C = {}
		for Yi in y:
			if Yi in C:
				C[Yi] += 1
			else:
				C[Yi] = 1
		maxY = -1
		for k in C:
			if C[k] > maxY:
				maxY = C[k]
				root.label = k
		return

	root.fIndex, root.fValue = minGiniOfF(x,y,f,fi)
	root.left = node()
	root.right = node()
	x1 = []
	y1 = []
	x2 = []
	y2 = []

	#should not be delete the used feature!!
	#bug ! 
	index = root.fIndex
	value = root.fValue
	del fi[index]
	print 'x',x
	for i,Xi in enumerate(x):
		if Xi[index] == value:
			x1.append(Xi)
			y1.append(y[i])
		else:
			x2.append(Xi)
			y2.append(y[i])
	buildOneNode(x1,y1,stopGini,root.left,f,fi)
	buildOneNode(x2,y2,stopGini,root.right,f,fi)
	return

def buildDecisionTree(x,y,stopGini):
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


x,y = loadTrainData('train.csv')
tree = buildDecisionTree(x,y,0.2)
for i,Xi in enumerate(x):
	Yi = predict(tree,Xi)
	if Yi == y[i]:
		print 'correct',i
	else:
		print 'error',i
	