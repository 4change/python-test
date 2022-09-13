#!/usr/bin/python
# -*- coding: UTF-8 -*-

# urllib2实现下载网页的3种方式
# 以python2的版本运行该代码

import cookielib
import urllib2
 
url = "http://www.baidu.com"
response1 = urllib2.urlopen(url)
print("第一种方法")
#获取状态码，200表示成功
print('状态码：' + str(response1.getcode()))
#获取网页内容的长度
print('网页内容长度：' + str(len(response1.read())))
 
print("第二种方法")
request = urllib2.Request(url)
#模拟Mozilla浏览器进行爬虫
request.add_header("user-agent","Mozilla/5.0")
response2 = urllib2.urlopen(request)
print('状态码：' + str(response2.getcode()))
print('网页内容长度：' + str(len(response2.read())))

print("第三种方法")
cookie = cookielib.CookieJar()
#加入urllib2处理cookie的能力
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
response3 = urllib2.urlopen(url)
print('状态码：' + str(response3.getcode()))
print('网页内容长度：' + str(len(response3.read())))
print('cookie: ' + str(cookie))
