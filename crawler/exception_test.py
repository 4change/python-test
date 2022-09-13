import urllib.request
import urllib.error

try:
    headers = {'User_Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}    
    response = urllib.request.Request('http://python.org/', headers=headers)
    html = urllib.request.urlopen(response)
    result = html.read().decode('utf-8')

except urllib.error.URLError as e:
    if hasattr(e, 'reason'):
        print('错误原因是：' + str(e.reason))

except urllib.error.HTTPError as e:
    if hasattr(e, 'code'):
        print('错误状态码是：' + str(e.code))
else:
    print('请求成功通过')
