from dataset import Dataset
from sklearn.metrics import mean_squared_error
import sys

class Node():
	def __init__(self):
		self.left_node = None
		self.right_node = None
		self.split_index = None
		self.split_value = None
		self.split_value_type = None
		self.leaf_value = None


class RegressionTree():
	def __init__(self,max_depth):
		self.max_depth = max_depth
		self.root = None
		self.real_type = 'real'
		self.unreal_type = 'unreal'

	def _square_error(self,y):
		try:
			mean = sum(y) / float(len(y))
			sum_se = sum(map(lambda yi:(yi-mean)**2,y))
		except ZeroDivisionError:
			sum_se = 0
		return sum_se

	def _get_split_values(self,col,value_type):
		# if value_type == self.real_type:
		# 	min_value = min(col)
		# 	max_value = max(col)
		# 	max_range = 10
		# 	interval = (max_value-min_value)/max_range
		# 	split_values = [min_value+i*interval for i in range(max_range)]
		# else:
		# 	split_values = list(set(col))
		split_values = list(set(col))
		return split_values

	def _is_left(self,value,split_value,value_type):
		if value_type == self.real_type:
			return value <= split_value
		else:
			return value == split_value

	def _construct_node(self,dataset,row_index,depth):
		"""construct node recursively"""
		if depth > self.max_depth:
			return None

		instances = dataset.get_instances(row_index)
		y = dataset.get_labels(row_index)

		square_error = self._square_error(y)

		best_split_index = None
		best_split_value = None
		best_split_type = None
		best_left_index = None
		best_right_index = None
		minimum_square_error = 2 ** 31.0

		value_type = None
		for col_index,field_type in enumerate(dataset.fields_type):
			if dataset.is_real_type(col_index):
				value_type = self.real_type
			else:
				value_type = self.unreal_type

			curr_col = dataset.get_column(instances,col_index)
			split_values = self._get_split_values(curr_col,value_type)
			for split_value in split_values:
				left_index = []
				right_index = []

				for row in row_index:
					x_instance = dataset.get_instance(row)

					if self._is_left(x_instance[col_index],split_value,value_type):
						left_index.append(row)
					else:
						right_index.append(row)

				left_square_error = self._square_error(dataset.get_labels(left_index))
				right_square_error = self._square_error(dataset.get_labels(right_index))
				sum_left_right_se = left_square_error + right_square_error
				if sum_left_right_se >= square_error:
					continue
				if sum_left_right_se < minimum_square_error:
					minimum_square_error = sum_left_right_se
					best_split_index = col_index
					best_split_value = split_value
					best_split_type = value_type
					best_left_index = left_index
					best_right_index = right_index

		node = Node()
		if best_split_index is not None:
			node.split_index = best_split_index
			node.split_value = best_split_value
			node.split_value_type = best_split_type

			node.left_node = self._construct_node(dataset,best_left_index,depth+1)
			node.right_node = self._construct_node(dataset,best_right_index,depth+1)
		
		if (node.left_node is None) and (node.right_node is None):
			node.leaf_value = sum(y) / float(len(y))
			print 'leaf node depth:{0}, leaf value:{1}'.format(depth,node.leaf_value)
			sys.stdout.flush() 

		return node

	def fit(self,dataset):
		row,col = dataset.shape
		self.root = self._construct_node(dataset,range(row),0)

	def _predict(self,node,x):
		if node.leaf_value is not None:
			return node.leaf_value
		else:
			if node.split_value_type == self.real_type:
				go_left = x[node.split_index] <= node.split_value
			else:
				go_left = x[node.split_index] == node.split_value

			if go_left:
				return self._predict(node.left_node,x)
			else:
				return self._predict(node.right_node,x)

	def predict(self,x):
		return self._predict(self.root,x)

if __name__ == '__main__':
	#test split function
	# regTree = RegressionTree(7)

	# real_value = [1.1,2.2,3.3,5.5,18.2,6.6,7.7]
	# cate_value = ['a','b','c','d','e','f','g']

	# real_split_value = regTree._get_split_values(real_value,regTree.real_type)
	# cate_split_value = regTree._get_split_values(cate_value,regTree.unreal_type)

	# print real_split_value
	# print cate_split_value
	
	from sklearn.datasets import make_friedman1
	X, y = make_friedman1(n_samples=1200, random_state=0, noise=1.0)
	X_train, X_test = X[:200], X[200:]
	y_train, y_test = y[:200], y[200:]
	dataset = Dataset()
	dataset.load_X_y(X_train,y_train)

	print dataset.fields_type
	sys.stdout.flush()

	regTree = RegressionTree(1)
	regTree.fit(dataset)

	testset = Dataset()
	testset.load_X_y(X_test,y_test)
	pred = []
	for x in testset.data:
		y = regTree.predict(x)
		pred.append(y)

	mse = mean_squared_error(testset.y,pred)
	print 'mean squared error is :{0}'.format(mse)
	f = open('pred.csv','w')
	for y in pred:
		f.write('{0}\n'.format(y))
	f.close()