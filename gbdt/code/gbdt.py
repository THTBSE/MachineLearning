from tree import RegressionTree
from random import Random

class LeastSquare():
	def loss(self,y,fx):
		Loss = sum([(yi-fxi)**2 for yi,fxi in zip(y,fx)])
		return Loss

	def negative_gradient(self,y,fx):
		"""calculate gradient of ls loss function"""
		g = [yi-fxi for yi,fxi in zip(y,fx)]
		return g


class GBDT():
	def __init__(self,n_estimators,learning_rate,max_depth,random_state,loss='ls',eta=0.5):
		self.n_estimators = n_estimators
		self.learning_rate = learning_rate
		self.max_depth = max_depth
		self.trees = []
		self.loss = loss
		self.loss_function = self._get_loss_function(self.loss)
		self.rng = Random(random_state)
		self.eta = eta

	def _get_loss_function(self,loss):
		if loss == 'ls':
			return LeastSquare()

	def _init_fx(self,y,loss):
		if loss == 'ls':
			mean = sum(y) / float(len(y))
			fx = [mean for yi in y]
			return fx

	def _subsampling(self,X,y):
		"""subsampling from X"""
		size = len(X)
		sample_num = int(self.eta * size)
		sample_index = self.rng.sample(range(size),sample_num)
		sub_X = [X[index] for index in sample_index]
		sub_y = [y[index] for index in sample_index]
		return sub_X,sub_y


	def fit(self,X,y):
		fx = [0 for yi in y]

		for m in range(self.n_estimators):
			Loss = self.loss_function.loss(y,fx)
			print 'epoch {0} ,loss:{1}'.format(m,Loss)

			rm = self.loss_function.negative_gradient(y,fx)
			tree = RegressionTree(self.max_depth)
			sub_X,sub_rm = self._subsampling(X,rm)
			tree.fit(sub_X,sub_rm)
			self.trees.append(tree)

			gamma_m = [tree.predict(x) for x in X]
			fx = [fxi+self.learning_rate*gamma_im for fxi,gamma_im in zip(fx,gamma_m)]

	def predict(self,x):
		pred = [tree.predict(x) for tree in self.trees]
		return sum(pred) * self.learning_rate


if __name__ == '__main__':
	from sklearn.datasets import make_friedman1
	from sklearn.metrics import mean_squared_error
	X, y = make_friedman1(n_samples=1200, random_state=0, noise=1.0)
	X_train, X_test = X[:200], X[200:]
	y_train, y_test = y[:200], y[200:]

	gbdt = GBDT(n_estimators=100,learning_rate=0.1,max_depth=1,random_state=0,loss='ls',eta=0.5)
	gbdt.fit(X_train,y_train)

	pred = [gbdt.predict(x) for x in X_test]

	mse = mean_squared_error(y_test,pred)
	print 'our classifier\'s mean squared error is :{0}'.format(mse)

	from sklearn.ensemble import GradientBoostingRegressor
	est = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,max_depth=1, random_state=0, loss='ls').fit(X_train, y_train)
	sklearn_mse = mean_squared_error(y_test, est.predict(X_test))
	print 'sklearn\'s classifier\'s mean squared error is :{0}'.format(sklearn_mse)

