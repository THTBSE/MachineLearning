import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestRegressor


def FilterData(df):
	df['time'] = df['datetime'].map(lambda x:float(x[11:13]))
	df.loc[df['humidity'] == 0,'humidity'] = df.loc[(df['season'] == 1) & (df['humidity'] != 0),'humidity'].median()
	for i in range(1,5):
		df.loc[(df['windspeed'] == 0) & (df['season'] == i),'windspeed'] = df.loc[(df['windspeed'] != 0) & \
		(df['season'] == i),'windspeed'].median()

	return df

def regularization(data,columnsIndex):
	for i in columnsIndex:
		rangeMax = data[:,i].max()
		rangeMin = data[:,i].min()
		data[:,i] = data[:,i] / (rangeMax - rangeMin)

labels = ['season','holiday','workingday','weather','temp','atemp','humidity','windspeed','time']
df = pd.read_csv('train.csv',header=0)
df = FilterData(df)

train_data = df.loc[:,labels]
train_data = train_data.values
n = train_data.shape[1]

regularization(train_data,range(n))

count = df.loc[:,'count']
count = count.values

clf = RandomForestRegressor(n_estimators = 200)
clf = clf.fit(train_data,count)

test_df = pd.read_csv('test.csv', header=0)
test_df = FilterData(test_df)

test_data = test_df.values
n = test_data.shape[1]

regularization(test_data,range(1,n))

result = clf.predict(test_data[:,1:])

output = open('results.csv','wb')
output.write('datetime,count\n')

for x,y in zip(test_data,result):
	output.write('{0},{1}\n'.format(x[0],int(y)))

output.close()
