#1.思考单页内容怎么爬取
#2.利用线程池爬取多页面
from concurrent.futures import ThreadPoolExecutor
import requests
import bs4
import re
import csv
import time
requests.packages.urllib3.disable_warnings()

#csv文件
f=open('电影天堂.csv','w',newline='',encoding='utf-8')
writer=csv.writer(f)

def get_name_dowloadlin(url):   
    resp=requests.get(url,verify=False)
    resp.encoding='gb2312'

    soup=bs4.BeautifulSoup(resp.text,'html.parser')
    list=soup.find("div",attrs={"class":"co_content8"})
    content=list.find("ul").find_all("table")

    #在content做re表达式
    obj=re.compile(r'<a class="ulink" href="(?P<url>.*?)" title="(?P<name>.*?)"',re.S)
        
    for i in content:
         j = i.find_all("a")
         for k in j:
            citer=obj.finditer(str(k))
            for match in citer:
                name=match.group('name')
                url=match.group('url')
                writer.writerow([name,url])

    print(url+'爬取完成')

if __name__=='__main__':
    #多线程爬取
    with ThreadPoolExecutor(50) as t:
        for i in range(1,21):
            url=f"https://www.dyttcn.com/kongbupian/list_6_{i}.html"
            t.submit(get_name_dowloadlin,url)
            time.sleep(1)

    print('前20页爬取完成')
    f.close()