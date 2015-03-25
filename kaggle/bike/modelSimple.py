import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

def pearson(x,y):
	N = x.shape[0]
	XDotY = np.dot(x.T,y)
	sumX = x.sum()
	sumY = y.sum()
	xSqrSum = (x ** 2).sum()
	ySqrSum = (y ** 2).sum()

	numerator = XDotY - (sumX * sumY / N)
	denominator = np.sqrt(xSqrSum - (sumX ** 2 / N)) * np.sqrt(ySqrSum - (sumY ** 2 / N))
	r = numerator / denominator
	return r


def FilterData(df):
	df['time'] = df['datetime'].map(lambda x:float(x[11:13]))
	df['year'] = df['datetime'].map(lambda x:int(x[0:4]))
	year = df['datetime'].map(lambda x:int(x[0:4]))
	month = df['datetime'].map(lambda x:int(x[5:7]))
	day = df['datetime'].map(lambda x:int(x[8:10]))
	weekday = []

	for y,m,d in zip(year,month,day):
		wd = datetime(y,m,d).weekday()
		weekday.append(wd)

	df['weekday'] = weekday
	df['year'] = year

	df.loc[df['humidity'] == 0,'humidity'] = df.loc[(df['season'] == 1) & (df['humidity'] != 0),'humidity'].mean()
	for i in range(1,5):
		df.loc[(df['windspeed'] == 0) & (df['season'] == i),'windspeed'] = df.loc[(df['windspeed'] != 0) & \
		(df['season'] == i),'windspeed'].mean()

	return df

def normalization(data,columnsIndex):
	for i in columnsIndex:
		rangeMax = data[:,i].max()
		rangeMin = data[:,i].min()
		data[:,i] = (data[:,i] - rangeMin) / (rangeMax - rangeMin)

labels = ['season','holiday','workingday','weather','temp','atemp','humidity','windspeed','time'\
,'year','weekday']
df = pd.read_csv('train.csv',header=0)
df = FilterData(df)

for label in labels:
	r1 = pearson(df[label].values,df['casual'].values)
	r2 = pearson(df[label].values,df['registered'].values)

	print '{0} with {1} is : {2}'.format(label,'casual',r1)
	print '{0} with {1} is : {2}'.format(label,'registered',r2)

train_data = df.loc[:,labels]
train_data = train_data.values

casual = df.loc[:,'casual'].values
register = df.loc[:,'registered'].values


clf_casual = RandomForestRegressor(n_estimators = 500,min_samples_split = 11)
clf_casual = clf_casual.fit(train_data,casual)

clf_register = RandomForestRegressor(n_estimators = 500,min_samples_split = 11)
clf_register = clf_register.fit(train_data,register)

test_df = pd.read_csv('test.csv', header=0)
test_df = FilterData(test_df)

test_datetime = test_df.loc[:,'datetime'].values
test_df = test_df.drop(['datetime'],axis=1)
test_data = test_df.loc[:,labels]
test_data = test_data.values
n = test_data.shape[1]


result_casual = clf_casual.predict(test_data)
result_register = clf_register.predict(test_data)

result = result_casual + result_register


output = open('results.csv','wb')
output.write('datetime,count\n')

for x,y in zip(test_datetime,result):
	output.write('{0},{1}\n'.format(x,int(y)))

output.close()
