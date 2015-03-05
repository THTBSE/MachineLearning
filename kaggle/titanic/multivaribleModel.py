import pandas as pd
import numpy as np 
from sklearn.ensemble import RandomForestClassifier

def filterData(df):
	df['Gender'] = df['Sex'].map({'female':0,'male':1})
	df['AgeFill'] = df['Age']

	median_ages = np.zeros((2,3))
	for i in range(0,2):
		for j in range(0,3):
			median_ages[i,j] = df.loc[(df['Gender'] == i) & (df['Pclass'] == j+1),'Age'].median()


	for i in range(0,2):
		for j in range(0,3):
			df.loc[(df.Age.isnull()) & (df['Gender'] == i) & (df['Pclass'] == j+1),'AgeFill'] = median_ages[i,j]


	df = df.drop(['Name','Sex','Age','Ticket','Cabin','Embarked'],axis=1)
	df.loc[df.Fare.isnull(),'Fare'] = df['Fare'].median()
	df['Age*Class'] = df.AgeFill * df.Pclass
	df['FamilySize'] = df.SibSp + df.Parch
	return df

df = pd.read_csv('train.csv',header=0)
df = filterData(df)
train_data = df.values

forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit(train_data[0::,2::],train_data[0::,1])

test_df = pd.read_csv('test.csv',header=0)
test_df = filterData(test_df)
test_data = test_df.values

output = forest.predict(test_data[0::,1::])

result = open('multimodel.csv','wb')
result.write('PassengerId,Survived\n')

for row0,row1 in zip(test_data[0::,0],output):
	result.write('{0},{1}\n'.format(int(row0),int(row1)))

result.close()

