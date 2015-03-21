import requests
import json
from collections import deque
import ConfigParser
import re
import time
import bs4
from bs4 import BeautifulSoup

session = None
cookies = {}
currTime = time.time()
qnum = re.compile(r'/question/(\d+)*')


def CreateSession():

    global session
    global cookies
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    
    cookies = cf._sections['cookies']
    
    email = cf.get("info", "email")
    password = cf.get("info", "password")

    cookies = dict(cookies)
    #print cookies
    
    s = requests.session()
    login_data = {'email': email, 'password': password}
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36",
        'Host': "www.zhihu.com",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }
    
    r = s.post('http://www.zhihu.com/login', data = login_data, headers = header)
    if r.json()["r"] == 1:
        print "Login Failed, reason is:"
        for m in r.json()["msg"]:
            print r.json()["msg"][m]
        print "Use cookies"
        has_cookies = False
        for key in cookies:
            if key != '__name__' and cookies[key] != '':
                has_cookies = True
                break
        if has_cookies == False:
            raise ValueError("请填写config.ini文件中的cookies项.")
    session = s

def GetFolloweesLists():
	global cookies
	global session

	urlList = []
	baseUrl = 'http://www.zhihu.com/people/heap_frank/followees'

	if session == None:
		CreateSession()
	s = session

	has_cookies = False
	for k in cookies:
		if k != '__name__' and cookies[k] != '':
			has_cookies = True
			r = s.get(baseUrl,cookies = cookies)
			break
	if has_cookies == False:
		r = s.get(baseUrl)

	soup = BeautifulSoup(r.content)
	_xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
	post_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
	hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]

	followeesCount = 88
	for i in range((followeesCount - 1) / 20 + 1):
		if i == 0:
			pl = soup.find_all('a',class_='zm-item-link-avatar')
			for p in pl:
				urlList.append(p['href'])
		else:
			offset = i * 20
			params = json.dumps({"offset": offset,"order_by":"created","hash_id": hash_id})
			data = {
			'_xsrf': _xsrf,
			'method': 'next',
			'params': params
			}
			header = {
			'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36",
			'Host': "www.zhihu.com",
			'Referer': baseUrl
			}
			has_cookies = False
			for key in cookies:
				if key != '__name__' and cookies[key] != '':
					has_cookies = True
					r_post = s.post(post_url, data = data, headers = header, cookies = cookies)
					break
			if has_cookies == False:
				r_post = s.post(post_url, data = data, headers = header)
			followees_list = r_post.json()["msg"]
			for p in followees_list:
				p_soup = BeautifulSoup(p)
				urlLink = p_soup.find('a',class_='zm-item-link-avatar')['href']
				urlList.append(urlLink)
	return urlList

def GetNews(user_url,hours):
	global cookies
	global session
	global currTime

	if session == None:
		CreateSession()
	s = session

	questionSet = set()
	postSet = set()

	has_cookies = False
	for k in cookies:
		if k != '__name__' and cookies[k] != '':
			has_cookies = True
			r = s.get(user_url,cookies = cookies)
			break
	if has_cookies == False:
		r = s.get(user_url)

	soup = BeautifulSoup(r.content)
	_xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
	post_url = user_url + '/activities'
	start = 0
	timelimits = 3600 * hours

	firstPage = soup.find_all('div',class_=['zm-profile-section-item','zm-item','clearfix'])
	for message in firstPage:
		if isinstance(message,bs4.element.Tag) and 'data-time' in message.attrs:
			dataTime = int(message['data-time'])
			start = dataTime
			if (currTime - dataTime) > timelimits:
				return questionSet,postSet
			qs = message.find('a',class_='question_link')
			ar = message.find('a',class_='post-link')
			if qs:
				match = qnum.match(qs['href'])
				if match:
					questionSet.add(match.group(1))
			if ar:
				postSet.add(ar['href'])

	header = {
	'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36",
	'Host': "www.zhihu.com",
	'Referer': user_url
	}

	while True:
		post_data = {'start':start,'_xsrf':_xsrf}
		if has_cookies:
			r_post = s.post(post_url,data = post_data, headers = header, cookies=cookies)
		else:
			r_post = s.post(post_url,data = post_data, headers = header)
		newsList = r_post.json()['msg']
		news_soup = BeautifulSoup(newsList[1])
		pages = news_soup.find_all('div',class_=['zm-profile-section-item','zm-item','clearfix'])
		for message in pages:
			if isinstance(message,bs4.element.Tag) and 'data-time' in message.attrs:
				dataTime = int(message['data-time'])
				start = dataTime
				if (currTime - dataTime) > timelimits:
					return questionSet,postSet
				qs = message.find('a',class_='question_link')
				ar = message.find('a',class_='post-link')
				if qs:
					match = qnum.match(qs['href'])
					if match:
						questionSet.add(match.group(1))
				if ar:
					postSet.add(ar['href'])
		if newsList[0] < 20:
			return questionSet,postSet

if __name__ == '__main__':
	CreateSession()
	urlList = GetFolloweesLists()
	baseUrl = 'http://www.zhihu.com'
	urlList = [baseUrl + postfix for postfix in urlList]

	indexTable = {}
	index = 1

	dataSet = []

	for url in urlList:
		qs,ps = GetNews(url,24)
		user = []
		for q in qs:
			if q in indexTable:
				user.append(indexTable[q])
			else:
				indexTable[q] = index
				user.append(index)
				index += 1
		for p in ps:
			if p in indexTable:
				user.append(indexTable[p])
			else:
				indexTable[p] = index
				user.append(index)
				index += 1
		if user:
			dataSet.append(user)
			print url
	urlTable = {}
	for k in indexTable:
		try:
			index = int(k)
			urlTable[indexTable[k]] = 'http://www.zhihu.com/question/' + k
		except ValueError:
			urlTable[indexTable[k]] = k

	f = open('dataSet.txt','w')
	for Set in dataSet:
		for data in Set:
			f.write('{0} '.format(data))
		f.write('\n')
	f.close()

	f = open('urlTable.txt','w')
	for k in urlTable:
		f.write('{0}\t{1}'.format(k,urlTable[k]))
		f.write('\n')
	f.close()
