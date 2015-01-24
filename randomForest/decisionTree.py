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
	print C
	sum = 0
	for k in C:
		p = float(C[k]) / numD
		p **= 2
		sum += p
	sum = 1 - sum
	print 'Gini(D) is:',sum
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
	print 'Gini(D,A) is:', Gini
	return Gini 

def minGiniOfAf(x,y,Af,index):
	minGini = 100000.0
	value = 0
	for A in Af: 
		Gini = GiniOfDA(x,y,A,index)
		if Gini < minGini:
			minGini = Gini
			value = A
	print 'minGini:',minGini,' feature index:',index,' feature value:',value
	return minGini, value

def minGiniOfF(x,y):
	numD = len(x)
	if (numD == 0):
		print 'input examples is empty'
		return -1,-1
	numF = len(x[0])
	f = [set([]) for i in range(numF)]
	for n in x:
		for i in range(numF):
			f[i].add(n[i])
	Gini = []
	Value = []
	for i,Af in enumerate(f):
		gini,value = minGiniOfAf(x,y,Af,i)
		Gini.append(gini)
		Value.append(value)
	minG = min(Gini)
	minIndex = Gini.index(minG)
	print 'min Gini:',minG
	return minIndex, Value[minIndex]

class node(object):
	def __init__(self):
		self.fIndex = None
		self.fValue = None
		self.left = None
		self.right = None
		self.label = None
	