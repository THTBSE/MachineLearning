
class Dataset():
	def __init__(self):
		self.data = None
		self.y = None
		self.fields_name = None
		self.fields_type = None
		self.shape = None

	def _get_field_type(self,value):
		if isinstance(value,int):
			return 'int'
		elif isinstance(value,float):
			return 'float'
		elif isinstance(value,str):
			try:
				int(value)
				return 'int'
			except ValueError:
				try:
					float(value)
					return 'float'
				except ValueError:
					return 'object'

	def load_from_file(self,file_path):
		#only csv format and do not hava missing value
		self.data = []
		self.y = []
		for line_cnt,line in enumerate(open(file_path)):
			if line_cnt == 0:
				self.fields_name = line.rstrip().split(',')
			else:
				fields_value = line.rstrip().split(',')
				if len(fields_value) != len(self.fields_name):
					raise ValueError("the number of fields must equal with indices!")
				
				if line_cnt == 1:
					self.fields_type = []
					for value in fields_value:
						self.fields_type.append(self._get_field_type(value))

				row = []
				for field_type,value in zip(self.fields_type,fields_value):
					try:
						if field_type == 'int':
							value = int(value)
						elif field_type == 'float':
							value = float(value)
					except ValueError:
						raise ValueError("cast error for:{0}".format(value))
					row.append(value)

				self.data.append(row[:-1])
				self.y.append(row[-1])

		self.fields_type = self.fields_type[:-1]
		self.shape = (len(self.data),len(self.fields_name[:-1]))

	def load_X_y(self,X,y):
		"""load dataset X and y, X must be a n * m Matrix, and y must be a n * 1 Matrix"""
		self.data = []
		self.y = []
		for row_x,row_y in zip(X,y):
			temp_x = []
			for xi in row_x:
				temp_x.append(xi)
			self.data.append(temp_x)
			self.y.append(row_y)

		first_row = self.data[0]
		self.fields_type = []
		for value in first_row:
			self.fields_type.append(self._get_field_type(value))

		self.shape = (len(self.data),len(self.fields_type))


	def get_instance(self,row_index):
		return self.data[row_index]

	def get_label(self,row_index):
		return self.y[row_index]

	def get_instances(self,row_index):
		"""return the row specified by row_index"""
		dataset = []
		for index in row_index:
			dataset.append(self.data[index])
		return dataset

	def get_labels(self,row_index):
		"""return the row label specified by row_index"""
		y = []
		for index in row_index:
			y.append(self.y[index])
		return y

	def get_column(self,matrix,col_index):
		"""get a specified column of a matrix"""
		return map(lambda row:row[col_index], matrix)

	def is_real_type(self,col_index):
		return self.fields_type[col_index] == 'float'




