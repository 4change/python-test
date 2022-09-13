import urllib.request

response = urllib.request.urlopen('http://python.org/')
# result = response.read()
result = response.read().decode('utf-8')    # utf-8解码
print(result)
