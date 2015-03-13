import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener) 

initUrl = 'http://www.zhihu.com/login'
content = urllib2.urlopen(initUrl).read()
soup = BeautifulSoup(content)

value = soup.find('input',type='hidden')
_xsrf = value['value']
print _xsrf

pdata = {'_xsrf':_xsrf,'email':'*******@qq.com','password':'*******','rememberme':'on'}
postdata = urllib.urlencode(pdata)

header = {'Referer':'http://www.zhihu.com',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'}

req = urllib2.Request(url='http://www.zhihu.com/login',data=postdata,headers=header)
print req
response = urllib2.urlopen(req)
text = response.read()

f = open('zhihu.html','wb')
f.write(text)
f.close()
