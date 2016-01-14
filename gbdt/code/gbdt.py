from tree import RegressionTree
from sklearn.tree import DecisionTreeRegressor
from random import Random
import math
import sys
import numpy as np

class LeastSquare():
	def loss(self,y,fx):
		Loss = sum([(yi-fxi)**2 for yi,fxi in zip(y,fx)])
		return Loss

	def negative_gradient(self,y,fx):
		"""calculate gradient of ls loss function"""
		g = [yi-fxi for yi,fxi in zip(y,fx)]
		return g

class MultinomialClass():
	def __init__(self,classes_=None):
		self.classes_ = classes_

	def _proba_of_classes(self,fxi):
		"""fxi is 1 row with K columns"""
		exp_class = [math.exp(f) for f in fxi]
		sum_exp_class = sum(exp_class)
		proba = [ek/sum_exp_class for ek in exp_class]
		return proba

	def negative_gradient(self,y,fx):
		"""fx is N*K matrix, K is the number of classes"""
		g = []
		for fxi,yi in zip(fx,y):
			proba = self._proba_of_classes(fxi)
			residual_i = [-p for p in proba]
			class_index = self.classes_.index(yi)
			residual_i[class_index] += 1
			g.append(residual_i)
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
		self.classes_ = None

	def _get_loss_function(self,loss):
		if loss == 'ls':
			return LeastSquare()
		elif loss == 'deviance':
			return None

	def _subsampling_index(self,size):
		"""return indices of subsampling"""
		sample_num = int(self.eta * size)
		sample_index = self.rng.sample(range(size),sample_num)
		return sample_index

	def _subsampling_A(self,A,sample_index):
		"""subsampling from A,A can be X or y"""
		sub_A = [A[index] for index in sample_index]
		return sub_A

	def _subsampling(self,X,y):
		"""subsampling from X,y"""
		sample_index = self._subsampling_index(len(X))
		sub_X = self._subsampling_A(X,sample_index)
		sub_y = self._subsampling_A(y,sample_index)
		return sub_X,sub_y

	def fit(self,X,y):
		if self.loss == 'deviance':
			classes_ = list(set(y))
			self.classes_ = classes_
			self.loss_function = MultinomialClass(classes_)

			#each class has a series of trees
			self.trees = [[] for k in classes_]

			#fx is a N*K matrix
			fx = [[0 for k in classes_] for i in y]

			#number of samples 
			n_samples = len(X)

			for m in xrange(self.n_estimators):
				print 'epoch {0}'.format(m)
				sys.stdout.flush()

				#subsample_index = self._subsampling_index(n_samples)
				#sub_X = self._subsampling_A(X,subsample_index)

				rm = self.loss_function.negative_gradient(y,fx)

				for k in range(len(classes_)):
					rmk = map(lambda a:a[k],rm)
					#tree = RegressionTree(self.max_depth)
					tree = DecisionTreeRegressor(max_depth=self.max_depth)
					#sub_rm = self._subsampling_A(rmk,subsample_index)

					tree.fit(X,rmk)
					#tree.fit(sub_X,sub_rm)
					self.trees[k].append(tree)
					print 'fit {0} trees done'.format(k)
					sys.stdout.flush()					

					gamma_mk = tree.predict(X)
					#gamma_mk = [tree.predict(x) for x in X]
					fxk = [fxi[k]+self.learning_rate*gamma_imk for fxi,gamma_imk in zip(fx,gamma_mk)]
					for fxi,next_fxik in zip(fx,fxk):
						fxi[k] = next_fxik


		else:
			fx = [0 for yi in y]

			for m in xrange(self.n_estimators):
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
		if self.loss == 'deviance':
			fx = [sum([tree.predict(x)[0] for tree in trees_k])*self.learning_rate for trees_k in self.trees]
			proba = self.loss_function._proba_of_classes(fx)
			index = proba.index(max(proba))
			return self.classes_[index]
		else:
			pred = [tree.predict(x) for tree in self.trees]
			r = sum(pred) * self.learning_rate
		return r


if __name__ == '__main__':
	# # # Test Regression
	# from sklearn.datasets import make_friedman1
	# from sklearn.metrics import mean_squared_error
	# X, y = make_friedman1(n_samples=1200, random_state=0, noise=1.0)
	# X_train, X_test = X[:200], X[200:]
	# y_train, y_test = y[:200], y[200:]

	# gbdt = GBDT(n_estimators=100,learning_rate=0.1,max_depth=1,random_state=0,loss='ls',eta=0.5)
	# gbdt.fit(X_train,y_train)

	# pred = [gbdt.predict(x) for x in X_test]

	# mse = mean_squared_error(y_test,pred)
	# print 'our regressor\'s mean squared error is :{0}'.format(mse)

	# from sklearn.ensemble import GradientBoostingRegressor
	# est = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,max_depth=1, random_state=0, loss='ls').fit(X_train, y_train)
	# sklearn_mse = mean_squared_error(y_test, est.predict(X_test))
	# print 'sklearn\'s regressor\'s mean squared error is :{0}'.format(sklearn_mse)

	# # # Test Classification
	from sklearn.datasets import load_iris
	from sklearn.datasets import make_hastie_10_2
	from sklearn.datasets import make_classification
	
	# # # Use hastie dataset
	# X,y = make_hastie_10_2(random_state=0)
	# print X.shape
	# X_train, X_test = X[:2000], X[2000:4000]
	# y_train, y_test = y[:2000], y[2000:4000]

	# # # Use iris dataset,which is multiclass
	# data = load_iris()
	# train_index = range(0,150,2)
	# test_index = range(1,150,2)
	# X_train, X_test = data['data'][train_index], data['data'][test_index]
	# y_train, y_test = data['target'][train_index], data['target'][test_index]

	# # # Use simple datasets
	X,y = make_classification(n_samples=1000,n_features=5,n_classes=4,n_clusters_per_class=1)
	X_train, X_test = X[:600], X[600:]
	y_train, y_test = y[:600], y[600:]

	gbdt_clf = GBDT(n_estimators=100,learning_rate=0.1,max_depth=1,random_state=0,loss='deviance',eta=0.5)
	gbdt_clf.fit(X_train,y_train)

	pred = [gbdt_clf.predict(x) for x in X_test]

	error_count = 0
	for y_true,y_pred in zip(y_test,pred):
		if y_true != y_pred:
			error_count += 1

	print 'error rate:',error_count/float(len(y_test))

	from sklearn.ensemble import GradientBoostingClassifier

	sk_clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0).fit(X_train, y_train)
	sk_pred = sk_clf.predict(X_test)

	error_count = 0
	for y_true,y_pred in zip(y_test,sk_pred):
		if y_true != y_pred:
			error_count += 1

	print 'error rate:',error_count/float(len(y_test))
	


