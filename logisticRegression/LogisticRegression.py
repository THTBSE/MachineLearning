import numpy as np 
import random

class LogisticRegression():
	def __init__(self,C,learning_rate='adadelta',eta0=0.5,eplison=1e-6,random_state=0,p=0.95,shuffle=True,max_iter=100):
		self.weights = None #w[0] is bias
		self.C = C
		self.learning_rate = learning_rate
		self.eta0 = eta0
		self.max_iter = max_iter
		self.eplison = eplison
		self.p = p
		self.shuffle = shuffle
		self.rng = random.Random(random_state)
		self.E_grad_square = 0
		self.E_deltaw_square = 0
		self.test_X = None
		self.test_y = None

	def _sigmoid(self,z):
		return (1.0 / (1 + np.exp(-z)))

	def _rms(self,z,eps=1e-6):
		return np.sqrt(z+eps)

	def _logloss(self,y,pred):
		loss = [-(yi*np.log(pred_i)+(1-yi)*np.log(1-pred_i)) + 0.5*self.C*np.dot(self.weights,self.weights) for yi,pred_i in zip(y,pred)]
		return sum(loss)

	def _error_rate(self,y,pred):
		error_num = len(filter(lambda a:a[0] != a[1],zip(y,pred)))
		return float(error_num) / len(y)


	def _adadelta(self,p,E_grad_square,E_deltaw_square,gradient):
		"""AdaDelta algorithm for calculating delta_w \
		where deltaa_w in formula:w[t+1] = w[t] + delta_w"""
		grad_square = np.square(gradient).sum()
		E_grad_square = p * E_grad_square + (1 - p) * grad_square
		coefficient = - self._rms(E_deltaw_square) / self._rms(E_grad_square) 
		delta_w = [coefficient * gi for gi in gradient]
		delta_w_square = np.square(delta_w).sum()
		E_deltaw_square = p * E_deltaw_square + (1 - p) * delta_w_square
		return delta_w,E_grad_square,E_deltaw_square 

	def _shuffle(self,X,y):
		shuffle_index = range(len(X))
		shuffle_index = self.rng.sample(shuffle_index,len(shuffle_index))
		X = [X[index] for index in shuffle_index]
		y = [y[index] for index in shuffle_index]
		return X,y

	def _insert_x0(self,x):
		"""insert x0 = 1 to x"""
		return [1] + list(x)

	def set_validate(self,X,y):
		"""specify the validate set"""
		self.test_X = np.copy(X)
		self.test_y = np.copy(y)

	def predict_proba(self,x):
		x = self._insert_x0(x)
		z = np.dot(self.weights,x)
		return self._sigmoid(z)

	def predict(self,x):
		prob_p = self.predict_proba(x)
		prob_n = 1 - prob_p
		if (prob_p - prob_n) > 0:
			return 1
		else:
			return 0

	def fit(self,X,y):
		if self.weights is None:
			dimension = len(X[0])
			self.weights = [self.rng.random() for i in range(dimension+1)] #x0=1,w[0]=bias

		prev_loss,prev_i = 2**31.0,0
		for i in range(self.max_iter):
			X,y = self._shuffle(X,y)
			for xi,yi in zip(X,y):
				xi = self._insert_x0(xi) #let x[0] = 1
				z = np.dot(self.weights,xi)
				pred_yi = self._sigmoid(z)
				residual = pred_yi - yi
				#g = (pred_yi - yi) * xi + C * w , where C * w is for regularization
				gradient = np.multiply(residual,xi) + np.multiply(self.C,self.weights)

				if self.learning_rate == 'adadelta':
					delta_w,self.E_grad_square,self.E_deltaw_square = self._adadelta(self.p,self.E_grad_square,self.E_deltaw_square,gradient)
				else:
					delta_w = [-self.eta0*gj for gj in gradient]
					self.eta0 *= self.p

				self.weights = [wj+delta_wj for wj,delta_wj in zip(self.weights,delta_w)]

			pred = [self.predict_proba(x) for x in self.test_X]
			loss = self._logloss(self.test_y,pred)
			print 'epoch:{0}, loss:{1}'.format(i,loss)
			if (i - prev_i) >= 50:
				delta_loss = loss - prev_loss
				if delta_loss > 0:
					break
				else:
					prev_loss = loss
					prev_i = i

		return self

def plotFig(w,dataSet,label):
	import matplotlib.pyplot as plt 
	set1 = []
	set2 = []


	for x,y in zip(dataSet,label):
		if y == 1:
			set1.append(x)
		else:
			set2.append(x)

	set1 = np.array(set1)
	set2 = np.array(set2)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(set1[:,0],set1[:,1],s=30,c='r',marker='s')
	ax.scatter(set2[:,0],set2[:,1],s=30,c='g')

	x = np.arange(-3.0,3.0,0.1)
	y = (-w[0] - w[1]*x)/w[2]
	ax.plot(x,y)
	plt.xlabel('X1')
	plt.ylabel('X2')
	plt.show()


if __name__ == '__main__':
	from sklearn.datasets import make_classification

	dataSet,label = make_classification(n_samples=500,n_features=2,n_redundant=0,n_clusters_per_class=1)
	train_X,train_y,test_X,test_y = dataSet[:400],label[:400],dataSet[400:],label[400:]
	clf = LogisticRegression(0.01,learning_rate='adadelta',shuffle=True,max_iter=500)
	clf.set_validate(test_X,test_y)
	clf = clf.fit(train_X[:100],train_y[:100])
	clf = clf.fit(train_X[100:200],train_y[100:200])
	clf = clf.fit(train_X[200:300],train_y[200:300])
	clf = clf.fit(train_X[300:],train_y[300:])
	weights = clf.weights
	print weights
	plotFig(weights,dataSet,label)