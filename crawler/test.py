# -*- coding:utf-8 -*-

import urllib2

response = urllib2.request.urlopen("http://www.baidu.com")
print(response.read())