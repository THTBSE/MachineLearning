import requests
import re
import time
import ConfigParser
import random
from bs4 import BeautifulSoup 

gm = re.compile(r'http://www.douban.com/group/(.*)/')
count = 0
cookies = {}
#header = {
#        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36",
#        'Host': "www.douban.com",
#   }
header = {}

def loadCookies():
	global cookies
	cf = ConfigParser.ConfigParser()
	cf.read('config.ini')
	cookies = cf._sections['cookies']
	cookies.pop('__name__')
	cookies = dict(cookies)
	header = cf._sections['headers']
	header.pop('__name__')
	header = dict(header)
	header['cookie'] = cookies

def loadInitURL(filename):
	url = [u.rstrip() for u in open(filename,'r')]
	return url 

def saveWord(wc,number):
	f = open('wc{0}.csv'.format(number),'w')
	f.write('word,count\n')
	for word in wc:
		f.write('{0},{1}\n'.format(word,wc[word]))
	f.close()

def getGroupURL(url):
	global count
	currUrl = url
	groupURL = []
	pageN = 1
	while True:
		page = requests.get(currUrl,headers=header)
		print pageN
		pageN += 1
		soup = BeautifulSoup(page.text)
		groups = soup.find_all('div',class_='result')
		if not groups:
			print 'sleep 1 seconds'
			time.sleep(1)
			pageN -= 1
			continue
		for group in groups:
			url = group.h3.a['href']
			groupURL.append(url)
		NEXT = soup.find('link',rel='next')
		if NEXT:
			nextURL = NEXT['href']
			currUrl = nextURL.replace('&amp;','&')
		else:
			break


	filename = 'url{0}.txt'.format(count)
	count += 1
	f = open(filename,'w')
	for gu in groupURL:
		f.write('{0}\n'.format(gu))
	f.close()
	return filename

def downloadPages(file):
	global cookies
	global header
	pageCount = 0
	groups = set([])
	for fn in files:
		f = open(fn,'r')
		for url in f.readlines():
			url = url.rstrip()
			gMatch = gm.match(url)
			if gMatch and (gMatch.group(1) not in groups):
				groups.add(gMatch.group(1))
				page = requests.get(url,headers=header,cookies=cookies)
				fs = open('pages/page{0}.html'.format(pageCount),'w')
				fs.write(page.text.encode('utf-8'))
				fs.close()
				print 'download page {0} done...'.format(pageCount)
				pageCount += 1
			time.sleep(0.5)
		f.close()
		print 'processing file {0} done...'.format(fn)

def downloadWebsites(filename,begNum = 0):
	f = open(filename,'r')
	urls = f.readlines()
	totalCount = len(urls)
	f.close()
	pageCount = begNum
	for i in xrange(pageCount,totalCount):
		url = urls[i].rstrip()
		print 'get page {0}'.format(url)
		page = requests.get(url,headers=header,cookies=cookies)
		print page.status_code
		fs = open('websites/page{0}.html'.format(pageCount),'w')
		fs.write(page.text.encode('utf-8'))
		fs.close()
		print 'download page {0} done...'.format(pageCount)
		pageCount += 1
		sleepTime = 0.5 + random.random() * 5
		time.sleep(sleepTime)
		print 'sleep {0} seconds over!'.format(sleepTime)

def filterURL(files):
	groups = set([])
	for fn in files:
		f = open(fn,'r')
		for url in f.readlines():
			count += 1
			url = url.rstrip()
			gMatch = gm.match(url)
			if gMatch and (gMatch.group(1) not in groups):
				groups.add(gMatch.group(1))
	fs = open('url.txt','w')
	for group in groups:
		fs.write('http://www.douban.com/group/{0}/\n'.format(group))
	fs.close()

def parsePages(pageCount):
	words = {}
	for i in range(pageCount):
		f = open('websites/page{0}.html'.format(i),'r')
		soup = BeautifulSoup(f)
		f.close()
		tags = soup.find('div',class_='group-tags')
		if tags:
			ts = tags.find_all('a',class_='tag')
			for tag in ts:
				word = tag.text.encode('gbk')
				words.setdefault(word,0)
				words[word] += 1
		print 'processing page {0} done!'.format(i)
	terms = words.items()
	terms.sort(key=lambda x:x[1],reverse=True)
	result = open('wc.csv','w')
	result.write('word,count\n')
	for wc in terms:
		result.write('{0},{1}\n'.format(wc[0],wc[1]))

def control():
	urls = loadInitURL('init.txt')
	files = []
	for url in urls:
		fn = getGroupURL(url)
		files.append(fn)

def merge(fs):
	words = {}
	for fn in fs:
		f = open(fn,'r')
		f.readline()
		for wc in f:
			w,c = wc.rstrip().split(',')
			c = int(c)
			words.setdefault(w,0)
			words[w] += c
	fn = open('merge.csv','w')
	fn.write('word,count\n')
	terms = words.items()
	terms.sort(key=lambda x:x[1],reverse=True)
	for term in terms:
		fn.write('{0},{1}\n'.format(term[0],term[1]))
	fn.close()



if __name__ == '__main__':
	#control()
	#loadCookies() 
	#files = ['url0.txt','url1.txt','url2.txt','url3.txt','url4.txt']
	#downloadPages(files)
	#filterURL(files)
	#downloadWebsites('url.txt',3167)
	#parsePages(3233)
	merge(['taobao.csv','meilishuo.csv'])