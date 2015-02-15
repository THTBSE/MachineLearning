import urllib2

def openWeb():
	req = urllib2.Request('http://www.baidu.com')

	try:
	 response = urllib2.urlopen(req)
	except urllib2.URLError, e:
		print e.reason
		return
	html = response.read()
	print html


if __name__ == '__main__':
	openWeb()
