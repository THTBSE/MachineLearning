
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

	def _get_fields_type(self,x):
		"""get every field type of an instance x"""
		fields_type = map(lambda xi:self.real_type if isinstance(xi,float) else self.unreal_type,x)
		return fields_type

	def _get_column(self,X,col_index):
		col = [row[col_index] for row in X]
		return col

	def _construct_node(self,X,y,depth):
		"""construct node recursively"""
		if depth > self.max_depth:
			return None

		square_error = self._square_error(y)

		best_split_index = None
		best_split_value = None
		best_split_type = None
		best_left_samples = None
		best_right_samples = None
		minimum_square_error = float(2**31)

		#scan for best split feature and point
		fields_type = self._get_fields_type(X[0])
		for col_index,field_type in enumerate(fields_type):
			curr_col = self._get_column(X,col_index)
			split_values = self._get_split_values(curr_col,field_type)
			for split_value in split_values:
				left_samples = {'X':[],'y':[]}
				right_samples = {'X':[],'y':[]}

				for x,yi in zip(X,y):
					if self._is_left(x[col_index],split_value,field_type):
						left_samples['X'].append(x)
						left_samples['y'].append(yi)
					else:
						right_samples['X'].append(x)
						right_samples['y'].append(yi)

				left_square_error = self._square_error(left_samples['y'])
				right_square_error = self._square_error(right_samples['y'])
				sum_left_right_se = left_square_error + right_square_error
				if sum_left_right_se < square_error and sum_left_right_se < minimum_square_error:
					minimum_square_error = sum_left_right_se
					best_split_index = col_index
					best_split_value = split_value
					best_split_type = field_type
					best_left_samples = left_samples
					best_right_samples = right_samples

		node = Node()
		if best_split_index is not None:
			node.split_index = best_split_index
			node.split_value = best_split_value
			node.split_value_type = best_split_type

			node.left_node = self._construct_node(best_left_samples['X'],best_left_samples['y'],depth+1)
			node.right_node = self._construct_node(best_right_samples['X'],best_right_samples['y'],depth+1)

		if (node.left_node is None) and (node.right_node is None):
			node.leaf_value = sum(y)/float(len(y))

		return node

	def fit(self,X,y):
		self.root = self._construct_node(X,y,0)

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
		"""predict the target value of an instance x"""
		return self._predict(self.root,x)

if __name__ == '__main__':
	from sklearn.datasets import make_friedman1
	from sklearn.metrics import mean_squared_error

	X, y = make_friedman1(n_samples=1200, random_state=0, noise=1.0)
	X_train, X_test = X[:200], X[200:]
	y_train, y_test = y[:200], y[200:]

	regTree = RegressionTree(max_depth=3)
	regTree.fit(X_train,y_train)

	pred = [regTree.predict(x) for x in X_test]

	mse = mean_squared_error(y_test,pred)
	print 'mean squared error is :{0}'.format(mse)
