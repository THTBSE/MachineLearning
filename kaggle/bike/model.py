import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestRegressor

def FilterData(df):
	df['time'] = df['datetime'].map(lambda x:float(x[11:13]))
	df['month'] = df['datetime'].map(lambda x:float(x[5:7]))

	return df


labels = ['season','holiday','workingday','weather','temp','atemp','humidity','windspeed','time']
df = pd.read_csv('train.csv',header=0)
df = FilterData(df)

trains = []
counts = []

for i in xrange(1,13):
	train_data = df.loc[df['month'] == i,labels]
	count = df.loc[df['month'] == i,'count']
	trains.append(train_data.values)
	counts.append(count.values)

models = []

for x,y in zip(trains,counts):
	clf = RandomForestRegressor(n_estimators = 50)
	clf.fit(x,y)
	models.append(clf)


#train_data = df.loc[:,labels]
#train_data = train_data.values

#count = df.loc[:,'count']
#count = count.values

#clf = RandomForestRegressor(n_estimators = 50)
#clf = clf.fit(train_data,count)

test_df = pd.read_csv('test.csv', header=0)
test_df = FilterData(test_df)

#test_data = test_df.values

result = []

for i in range(12):
	test_data = test_df.loc[test_df['month'] == i+1,labels]
	test_data = test_data.values
	prediction = models[i].predict(test_data)
	result.append(prediction)
#result = clf.predict(test_data[:,1:])

output = open('results.csv','wb')
output.write('datetime,count\n')

#for x,y in zip(test_data,result):
#	output.write('{0},{1}\n'.format(x[0],int(y)))
for i in range(12):
	date = test_df.loc[test_df['month'] == i+1,'datetime']
	m = result[i]
	for data,date in zip(m,date):
		output.write('{0},{1}\n'.format(date,int(data)))

output.close()
