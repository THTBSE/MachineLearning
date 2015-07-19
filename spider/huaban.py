import json 
import requests
import re
import sys
import os
import time

imgCount = 200
keyword = None
pattern = re.compile(r'^a.+\["(\w+)"\]')

def save_img(imgURL,filePath,imgName,imgSuffix):
	img = requests.get(imgURL)
	if not img.ok:
		print 'can not get image'
		return

	if filePath[-1] == '/':
		filePath = filePath + imgName + '.' + imgSuffix
	else:
		filePath = filePath + '/' + imgName + '.' + imgSuffix

	f = open(filePath,'wb')
	f.write(img.content)
	f.close()

def load_config(filePath):
	config = {}
	f = open(filePath,'r')
	for line in f:
		line = line.rstrip().split('=')
		if len(line) < 2:
			continue
		config[line[0]] = line[1]
	f.close()
	return config

def get_pins_jstring(text):
	for line in text:
		if (len(line) < 16) or (line[0:16] != 'app.page["pins"]'):
			continue
		line = line.rstrip().split(' = ')
		return line[1][:-1]

def get_base_info(text):
	global pattern
	info = {}
	for line in text:
		if (len(line) < 3) or (line[0:3] != 'app'):
			continue
		line = line.rstrip().split(' = ')
		m = pattern.match(line[0])
		if not m:
			continue
		term = m.group(1)
		if term == 'settings':
			jo = json.loads(line[1][:-1])
			info['imgHosts'] = 'http://' + jo['imgHosts']['hbimg']
		elif term == 'facets':
			jo = json.loads(line[1][:-1])
			info['total'] = int(jo['total'])
		elif term == 'pins':
			info['jstring'] = get_pins_jstring(text)
	return info

def get_img_info(jstring):
	images = []
	jarray = json.loads(jstring)
	for obj in jarray:
		img = {}
		try:
			img['key'] = obj['file']['key'].encode('utf-8')
			img['type'] = obj['file']['type'][6:].encode('utf-8')
			images.append(img)
		except KeyError, e:
			print 'KeyError'
	return images

def main():
	url = 'http://huaban.com/search/?q='
	config = load_config('config')
	imgCount = int(config['count'])
	keyword = config['keyword']
	savePath = config['savepath']
	url += keyword
	dirname = time.ctime().replace(' ','-').replace(':','-')
	savePath = savePath + '/' + dirname
	os.mkdir(savePath)
	res = requests.get(url)
	if not res.ok:
		print 'can not connect to huaban...'
		return
	text = res.text.split('\n')
	info = get_base_info(text)
	if imgCount > info['total']:
		imgCount = info['total']

	print imgCount
	currImgCount = 0
	jstring = info['jstring']
	imgs = []
	page = 1
	while (currImgCount < imgCount):
		images = get_img_info(jstring)
		imgs.extend(images)

		currImgCount = len(imgs)
		print 'get {0} images...'.format(currImgCount)
		sys.stdout.flush()

		page += 1
		newUrl = url + '&page=' + str(page) + '&per_page=20&wfl=1'
		res = requests.get(newUrl)
		jstring = get_pins_jstring(res.text.split('\n'))

	save_count = 0
	for img in imgs[:imgCount]:
		save_img(info['imgHosts']+'/'+img['key'],savePath,img['key'],img['type'])
		save_count += 1
		print 'save {0} imgs...'.format(save_count)
		sys.stdout.flush()

if __name__ == '__main__':
	main()


	
