import numpy as np 
from sklearn.naive_bayes import GaussianNB

#装载词袋，可能会有空的词，需要排除
def loadWordBag(fpath):
	words = {}
	dim = 0
	f = open(fpath,'r')
	seg = f.readline()
	seg = seg.split(' ')
	for word in seg:
		if word:
			words[word] = dim
			dim += 1
	return words

#将已分词的文档转换为一个矢量
def doc2Vec(filename,wordBag):
	dim = len(wordBag)
	f = open(filename,'r')
	examples = []
	for line in f:
		vec = np.zeros(dim)
		words = line.rstrip().split(' ')
		for word in words:
			if word in wordBag:
				vec[wordBag[word]] = 1
		examples.append(vec)
	f.close()
	return examples

#根据词频来设置文档向量
def doc2VecByTF(filename,wordBag):
	dim = len(wordBag)
	f = open(filename,'r')
	examples = []
	for line in f:
		vec = np.zeros(dim)
		words = line.rstrip().split(' ')
		for word in words:
			if word in wordBag:
				vec[wordBag[word]] = float(words.count(word)) / len(words)
		#l2norm = np.linalg.norm(vec,2)
		#if l2norm > 1e-3:
		#	vec = vec / l2norm
		examples.append(vec)
	f.close()
	return examples

#根据tf-idf来设置文档向量
def doc2VecByTFIDF(filename,wordBag):
	pass

#载入数据（训练、测试）并转换为矢量，分开载入，因为两类的内容分两个文本存放
#file1为类型1的样本，file0为类型0的样本
def loadData(file1,file0,wordBag,doc2Vec):
	data1 = doc2Vec(file1,wordBag)
	data0 = doc2Vec(file0,wordBag)
	count1 = len(data1)
	count0 = len(data0)
	
	label1 = np.ones(count1).tolist()
	label0 = np.zeros(count0).tolist()

	data1.extend(data0)
	label1.extend(label0)

	return data1,label1

def trainClassifier(training_data,labels):
	gnb = GaussianNB()
	gnb = gnb.fit(training_data,labels)
	return gnb 

#保存训练后的分类器参数与词袋，便于用java载入进行分类
def saveClassifier(nb,wordBag,savePath):
	f = open(savePath,'w')
	f.write('wordBag\t')
	words = wordBag.items()
	words.sort(key=lambda x:x[1])
	for word in words[:-1]:
		f.write('{0},'.format(word[0]))
	f.write('{0}\n'.format(words[-1][0]))
	f.write('Class\t')
	f.write('{0},{1}\n'.format(nb.class_prior_[0],nb.class_prior_[1]))

	f.write('Sigma\t')
	sigma = nb.sigma_
	for sigmai in sigma:
		for num in sigmai[:-1]:
			f.write('{0},'.format(num))
		f.write('{0} '.format(sigmai[-1]))
	f.write('\n')

	theta = nb.theta_
	f.write('Theta\t')
	for thetai in theta:
		for num in thetai[:-1]:
			f.write('{0},'.format(num))
		f.write('{0} '.format(thetai[-1]))
	f.close()

def saveDocVec(data,label,savePath):
	f = open(savePath,'w')
	for x,y in zip(data,label):
		for n in x:
			f.write('{0},'.format(n))
		f.write('{0}\n'.format(y))
	f.close()



if __name__ == '__main__':
	#wordBag = loadWordBag('newFW.txt')
	wordBag = loadWordBag('featureWords.txt')
	train_data,train_label = loadData('CommerceWord.txt','NotCommerceWord.txt',wordBag,doc2VecByTF)
	test_data,test_label = loadData('testCWord.txt','testNCWord.txt',wordBag,doc2VecByTF)

	gnb = trainClassifier(train_data,train_label)

	saveClassifier(gnb,wordBag,'cls.txt')
	saveDocVec(test_data,test_label,'testdata.txt')

	pred = gnb.predict(test_data)
	#pred = gnb.predict(train_data)

	count = 0
	for p,y in zip(pred,test_label):
	#for p,y in zip(pred,train_label):
		if p != y:
			count += 1

	#train_data_count = len(train_data)
	#errorRate = float(count) / train_data_count
	#print 'Test {0} examples,error rate is :{1} '.format(train_data_count,errorRate)
	test_data_count = len(test_data)
	errorRate = float(count) / test_data_count
	print 'Test {0} examples,error rate is :{1} '.format(test_data_count,errorRate)


#	f = open('CommerceVec.txt','w')
#	for x in examples:
#		x = x.tolist()
#		for n in x:
#			f.write('{0},'.format(n))
#		f.write('C\n')


