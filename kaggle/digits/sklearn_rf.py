from sklearn.ensemble import RandomForestClassifier

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
	print 'loadTrainData done'
	return x,y

def loadTestData(filename):
	f = open(filename,'r')
	f.readline()
	x = []
	for line in f.readlines():
		line = line.split(',')
		x.append([int(n) for n in line])
	print 'loadTestData done'
	return x

x,y = loadTrainData('train.csv')
forest = RandomForestClassifier(n_estimators = 1000)
print 'establish rfc done'
forest.fit(x,y)
print 'fit dataSet done'
xTest = loadTestData('test.csv')

rf = open('rf_result.csv','w')
rf.write('ImageId,Label\n')
for i,Xi in enumerate(xTest):
	yi = forest.predict(Xi)
	rf.write(str(i+1))
	rf.write(',')
	rf.write(str(yi[0]))
	rf.write('\n')