import re
import urllib
from urllib import request

url = "http://mm.taobao.com/631300490.htm"
print(request.urlopen(url).read().decode('gbk'))
