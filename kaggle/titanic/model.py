import numpy as np
import csv

csv_file_object = csv.reader(open('train.csv','rb'))
header = csv_file_object.next()

data = [row for row in csv_file_object]
data = np.array(data)

women_only_stats = data[0::,4] == 'female'

men_only_stats = data[0::,4] != 'female'

women_onboard = data[women_only_stats,1].astype(np.float)

men_onboard = data[men_only_stats,1].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who survived is {0}'.format(proportion_women_survived)
print 'Proportion of women who survived is {0}'.format(proportion_men_survived)

test_file_object = csv.reader(open('test.csv','rb'))
header = test_file_object.next()

prediction_file = open('gendermodel.csv','wb')
prediction_file_object = csv.writer(prediction_file)

prediction_file_object.writerow(['PassengerId','Survived'])

for row in test_file_object:
	if row[3] == 'female':
		prediction_file_object.writerow([row[0],'1'])
	else:
		prediction_file_object.writerow([row[0],'0'])

prediction_file.close()

