import requests
import re
import json
from pprint import pprint
url="https://www.acfun.cn/v/ac45606599"

obj = re.compile('window.pageInfo = window.videoInfo =(.*?);',re.S)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Referer':'https://www.acfun.cn/'
}

resp=requests.get(url,headers=headers)

result=obj.findall(resp.text)[0]

dic=json.loads(result)

title=dic['title']
u=json.loads(dic['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['url']

resp2=requests.get(u,headers=headers)

data=resp2.text

#print(data)
obj1 = re.compile(r'#EXTINF:.*?,\n(.*?)\n',re.S)
result1=obj1.findall(data)


for i in result1:
    domain="https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/"
    resp3=requests.get(domain+i,headers=headers)
    with open(title+'.mp4','ab') as f:
        f.write(resp3.content)