import numpy as np 
import sys

def loadDoc(filePath):
	f = open(filePath,'r')
	doc = []
	for line in f:
		words = line.rstrip().split(' ')
		doc.append(words)
	f.close()
	return doc

def tf(doc):
	words = {}
	total = 0
	for line in doc:
		for word in line:
			words.setdefault(word,0)
			words[word] += 1
			total += 1
	total = float(total)
	for w in words:
		words[w] /= total
	return words

def idf(doc):
	docCount = float(len(doc))
	words_idf = {}
	for line in doc:
		uniqueWords = set(line)
		for w in uniqueWords:
			words_idf.setdefault(w,0)
			words_idf[w] += 1
	for w in words_idf:
		words_idf[w] = np.log(docCount / (words_idf[w]+1))
	return words_idf

def tf_idf(tf,idf):
	tfidf = {}
	for w in tf:
		tfidf[w] = tf[w] * idf[w]
	return tfidf

def outputTF_IDF(tfidf,cat):
	if cat == 'c':
		f = open('commerce_tfidf.txt','w')
	elif cat == 'nc':
		f = open('not_commerce_tfidf.txt','w')
	words_tfidf = tfidf.items()
	words_tfidf.sort(key=lambda x:x[1],reverse=True)
	for word in words_tfidf:
		f.write('{0}:{1}\n'.format(word[0],word[1]))
	f.close()


def extractFeatureWords(cata1,cata2,rank=100):
	cata1_words = cata1.items()
	cata2_words = cata2.items()

	cata1_words.sort(key=lambda x:x[1],reverse=True)
	cata2_words.sort(key=lambda x:x[1],reverse=True)

	wordSet1 = set([w[0] for w in cata1_words[:rank]])
	wordSet2 = set([w[0] for w in cata2_words[:rank]])

	words = wordSet1.union(wordSet2).difference(wordSet1.intersection(wordSet2))
	words = list(words)
	return words

if __name__ == '__main__':
	if len(sys.argv) >= 3:
		commercePath = sys.argv[1]
		notCommercePath = sys.argv[2]

		comDoc = loadDoc(commercePath)
		notComDoc = loadDoc(notCommercePath)

		tfidf = {}
		tfidf['c'] = tf(comDoc)
		tfidf['nc'] = tf(notComDoc)

		comDoc.extend(notComDoc)
		idf_ = idf(comDoc)

		tfidf['c'] = tf_idf(tfidf['c'],idf_)
		tfidf['nc'] = tf_idf(tfidf['nc'],idf_)

		outputTF_IDF(tfidf['c'],'c')
		outputTF_IDF(tfidf['nc'],'nc')

		featureWords = extractFeatureWords(tfidf['c'],tfidf['nc'],85)
		f = open('newFW.txt','w')
		for word in featureWords[:-1]:
			f.write('{0} '.format(word))
		f.write('{0}'.format(featureWords[-1]))
		f.close()
