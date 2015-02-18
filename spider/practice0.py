import urllib2
import re

#a simple spider for practice 
def openWeb():
	req = urllib2.Request('http://www.zhihu.com/search?q=python&type=question')
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) \
	AppleWebKit/537.36 (KHTML, like Gecko) \
	Chrome/42.0.2298.0 Safari/537.36'}
	req.add_header('User-Agent',headers['User-Agent'])
	try:
	 response = urllib2.urlopen(req)
	except urllib2.URLError, e:
		print e.reason
	else:
		html = response.read()
		pattern = re.compile('/question/\d+')
		head = 'http://www.zhihu.com'
		qset = set([])
		for m in pattern.finditer(html):
			qset.add(head+m.group())
		for i,q in enumerate(qset):
			subresponse = urllib2.urlopen(q)
			f = open('{0}Q.html'.format(i),'w')
			f.write(subresponse.read())
			f.close()
if __name__ == '__main__':
	openWeb()
