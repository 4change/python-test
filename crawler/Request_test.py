import urllib.request

headers = {'User_Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
response = urllib.request.Request('http://python.org', headers=headers)
html = urllib.request.urlopen(response)
result = html.read().decode('utf-8')
print(result)
