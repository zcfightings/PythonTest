import re
import urllib
from urllib import request

url = r"""hello
"""

pattern = re.compile('<a target=\'_blank\' href=\'(.*?)\'>(.*?)</a></b></font><font size=',re.S)

items = re.findall(pattern,url)
for item in items :
    print(item[0], item[1])

