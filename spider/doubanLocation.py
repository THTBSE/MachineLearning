import bs4
import urllib2
import re
from bs4 import BeautifulSoup

__author__ = 'Frank'

digit = re.compile(r'(\d+)')

def GetEventTag(Soup,events):
	li = Soup.find('li',class_='list-entry')
	events.append(li)
	for sibling in li.next_siblings:
		if (isinstance(sibling,bs4.element.Tag)) & (sibling.name == 'li'):
			events.append(sibling)
	return events

def GetEventInfo(event):
	eventInfo = {}
	#get the poster of event
	img = event.find('img')
	eventInfo['Poster'] = img['data-lazy']
	#get the title and url of event
	info = event.find('div',class_='title').find('a')
	eventInfo['Title'] = unicode(info['title']).encode('utf-8')
	eventInfo['URL'] = info['href']
	#get the time of event
	times = event.find('li',class_='event-time').find_all('time')
	for time in times:
		if time['itemprop'] == 'startDate':
			eventInfo['StartDate'] = time['datetime']
		elif time['itemprop'] == 'endDate':
			eventInfo['EndDate'] = time['datetime']
	#get the location of event
	location = event.find('meta',itemprop='location')
	eventInfo['Location'] = unicode(location['content']).encode('utf-8')
	#get the fee of event
	fee = event.find('li',class_='fee').find('strong')
	fee = unicode(fee.string).encode('utf-8')
	feeNum = digit.match(fee)
	if feeNum:
		eventInfo['Fee'] = feeNum.group(1)
	else:
		eventInfo['Fee'] = '0'
	#get the owner of event
	#owner = event.find('a',class_='db-event-owner')
	#eventInfo['ownerURL'] = owner['href']
	#eventInfo['owner'] = owner.string.encode('utf-8')
	#get the counts of event
	count = event.find('p',class_='counts').find_all('span')
	for c in count:
		num = digit.match(unicode(c.string).encode('utf-8'))
		if not num:
			continue
		if 'Joined' in eventInfo:
			eventInfo['Interested'] = num.group(1)
		else:
			eventInfo['Joined'] = num.group(1)
	return eventInfo

BaseURL = 'http://www.douban.com/location/xiamen/events/future-all'
URL = 'http://www.douban.com/location/xiamen/events/future-all'

#initialHtml = open('c:/douban.html','rb')
initialHtml = urllib2.urlopen(URL).read()
Soup = BeautifulSoup(initialHtml)
#initialHtml.close()

totalPage = int(Soup.find('span',class_='thispage')['data-total-page'])
events = []
for i in xrange(totalPage):
	events = GetEventTag(Soup,events)
	pagination = Soup.find('span',class_='next')
	URL = pagination.find('link',rel='next')
	if URL:
		URL = BaseURL + URL['href']
		print URL
		initialHtml = urllib2.urlopen(URL).read()
		Soup = BeautifulSoup(initialHtml)
	else:
		break

infos = []
for event in events:
	info = GetEventInfo(event)
	infos.append(info)

files = open('result.csv','wb')

kw = ['Title','StartDate','EndDate','Location','Fee','Joined','Interested','URL','Poster']
files.write('Title,StartDate,EndDate,Location,Fee,Joined,Interested,URL,Poster\n')

for info in infos:
	for label in kw:
		if label != 'Poster':
			files.write('{0},'.format(info[label]))
		else:
			files.write('{0}\n'.format(info[label]))

files.close()

