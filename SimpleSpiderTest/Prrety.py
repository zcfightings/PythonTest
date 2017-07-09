import http
import urllib
from urllib import request
import re
import os



__author__ = 'zhaochen'


class UrlTool:
    pattern = re.compile('<a target=\'_blank\' href=\'(.*?)\'>(.*?)</a></b></font><font size=',re.S)

    def getItems(self,content):
        return re.findall(self.pattern,content)



class Prrety:


    def __init__(self,url,encoding,dir):
        self.baseURL = url
        self.encoding = encoding
        self.tool = UrlTool()
        self.basedir = dir

    def getPage(self, pageIndex):
        header = {}
        url = self.siteURL + "?page=" + str(pageIndex)
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        request.install_opener(opener)
        req = urllib.request.Request(url)
        response = request.urlopen(req)
        return response.read().decode(self.encoding)

    def getItems(self,page):
        return self.tool.getItems(page)


    def save2file(self,content,name):
        path = self.basedir + '/'+name+'.txt'
        file = open(path,'wb+')
        file.write(content)
        file.close()



