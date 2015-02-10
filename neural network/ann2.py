import random
import numpy as np

def sigmoid(z):
	return 1.0 / (1.0 + np.exp(-z))

sigmoid_vec = np.vectorize(sigmoid)

def sigmoid_prime(z):
	return sigmoid(z) * (1 - sigmoid(z))

sigmoid_prime_vec = np.vectorize(sigmoid_prime)

class QuadraticCost():
	@staticmethod
	def fn(a, y):
		return 0.5*np.linalg.norm(a-y)**2
	@staticmethod
	def delta(z, a, y):
		return (a - y) * sigmoid_prime_vec(z)

class CrossEntropyCost():
	@staticmethod
	def fn(a, y):
		return np.nan_to_num(np.sum(-y*np.log(a)-(1-y)*np.log(1-a)))
	@staticmethod
	def delta(z, a, y):
		return (a - y)

class ann2():
	def __init__(self, sizes, cost = CrossEntropyCost):
		self.num_of_layers = len(sizes)
		self.sizes = sizes
		self.cost = cost
		self.default_weight_initializer()

	def default_weight_initializer(self):
		self.biases = [np.random.randn(y,1) for y in self.sizes[1:]]
		self.weights = [np.random.randn(y,x) / np.sqrt(x) for y,x in zip(self.sizes[1:], self.sizes[:-1])]

	def large_weight_initializer(self):
		self.biases = [np.random.randn(y,1) for y in self.sizes[1:]]
		self.weights = [np.random.randn(y,x) for y,x in zip(self.sizes[1:], self.sizes[:-1])]

	def feedforward(self, a):
		for b, w in zip(self.biases, self.weights):
			a = sigmoid_vec(np.dot(w,a) + b)
		return a

	def SGD(self, training_data, epochs, mini_batch_size, eta, lmbda = 0.0, test_data = None):
		n = len(training_data)
		if test_data:
			ntest = len(test_data)
		for j in xrange(epochs):
			random.shuffle(training_data)
			mini_batches = [training_data[k:k+mini_batch_size] for k in xrange(0,n,mini_batch_size)]
			for mini_batch in mini_batches:
				self.update_mini_batch(mini_batch, eta, lmbda, n)
			if test_data:
				print "Epoch {0} {1} / {2}".format(j,self.evaluate(test_data), ntest)
			else:
				"Epoch {0} complete".format(j)

	def update_mini_batch(self, mini_batch, eta, lmbda, n):
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]

		for x,y in mini_batch:
			delta_b, delta_w = self.backprop(x,y)
			nabla_b = [b+nb for b,nb in zip(nabla_b, delta_b)]
			nabla_w = [w+nw for w,nw in zip(nabla_w, delta_w)]

		m = len(mini_batch)
		self.biases = [b - (eta * db) / m for b,db in zip(self.biases, nabla_b)]
		self.weights = [(1-(eta*lmbda)/n)*w - (eta*dw)/m for w,dw in zip(self.weights, nabla_w)]

	def backprop(self, x, y):
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]

		activation = x
		activations = [x]
		zs = []

		#feedforward
		for b,w in zip(self.biases, self.weights):
			z = np.dot(w, activation) + b
			activation = sigmoid_vec(z)
			activations.append(activation)
			zs.append(z)
		#back propagate
		delta = self.cost.delta(zs[-1], activations[-1], y)
		nabla_b[-1] = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())
		for l in xrange(2,self.num_of_layers):
			spv = sigmoid_prime_vec(zs[-l])
			delta = np.dot(self.weights[-l+1].transpose(), delta) * spv
			nabla_b[-l] = delta
			nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())

		return (nabla_b,nabla_w)

	def evaluate(self, test_data):
		test_results = [(np.argmax(self.feedforward(x)),np.argmax(y)) for x,y in test_data]
		return sum(int(x == y) for x,y in test_results)

	def predict(self, data):
		results = [np.argmax(self.feedforward(x)) for x in data]
		return results






