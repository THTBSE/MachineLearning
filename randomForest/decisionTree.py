
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

def GiniOfDA(x,y,A):
	GiniDA = []
	for a in A:
		
	GiniD1 = GiniOfD(y1)
	GiniD2 = GiniOfD(y2)
	numD = len(y)
	numD1 = len(y1)
	numD2 = len(y2)
	Gini = (float(numD1) / numD) * GiniD1 + (float(numD2) / numD) * GiniD2
	print 'Gini(D,A) is:', Gini
	return Gini 

class node(object):
	def __init__(self):
		self.fIndex = None
		self.fValue = None
		self.left = None
		self.right = None
		self.label = None
	