
def textStat(text):
	words = {}
	for w in text:
		words.setdefault(w,0)
		words[w] += 1
	return words

def similarity(text1,text2):
	wc1 = float(reduce(lambda x,y:x+y,[n[1] for n in text1.items()],0))
	wc2 = float(reduce(lambda x,y:x+y,[n[1] for n in text2.items()],0))

	s1 = set(text1.keys())
	s2 = set(text2.keys())

	intersection = s1.intersection(s2)
	repeat = []

	for w in intersection:
		x = min(text1[w],text2[w])
		repeat.append(x)

	rate = reduce(lambda x,y:x+y,repeat,0) / max(wc1,wc2)
	return rate

def loadText(fpath):
	f = open(fpath,'r')
	text = [] 
	for line in f:
		line = line.rstrip().split(' ')
		text.append(line)
	return text

if __name__=='__main__':
	raw = loadText('spam.txt')
	text = []
	for t in raw:
		text.append(textStat(t))
	for t in text:
		rate = similarity(text[0],t)
		print 'similarity rate is:{0}'.format(rate)



