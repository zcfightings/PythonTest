import urllib
from urllib import request
from urllib import error
import http.cookiejar
import re


user_agent = 'Mozilla/5.0'
headers = {'User-Agent':user_agent}
try:

    # url = 'http://www.qiushibaike.com/hot/page/2/'
    # req = request.Request(url,headers = headers)
    # response = urllib.request.urlopen(req)
    # content = response.read().decode('utf-8')
    # pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
    #                  '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats".*?class="number">(.*?)</i>',re.S)
    # items = re.findall(pattern,content)
    # for item in items:
    #     hasImage = re.search('img',item[3])
    #     if  hasImage:
    #         print(item[0],item[1],item[2],item[4])

    url = 'http://www.baidu.com'

    print('第一种方法')
    response1 = request.urlopen(url)
    print(response1.getcode())
    print(len(response1.read()))

    print('第二种方法')
    req = request.Request(url)
    req.add_header('user-agent',user_agent)
    response2 = request.urlopen(req)
    print(response2.getcode())
    print(len(response2.read()))

    print('第三种方法')
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    request.install_opener(opener)
    response3 = request.urlopen(url)
    print(response3.getcode())
    print(response3.read())





except error.URLError as e:
    if(hasattr(e,"code")):
        print(e.code)
    if(hasattr(e,"reason")):
        print(e.reason)

