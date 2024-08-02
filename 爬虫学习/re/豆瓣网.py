import re
import requests
import csv   #csv模块用于写入数据到csv文件,以 ',' 为分隔符
#拿到页面源代码
#根据re来提取需要的信息

url="https://movie.douban.com/top250"
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}
response=requests.get(url,headers=headers)

#页面源代码
page_content=response.text

#解析数据
obj=re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'   #re.S表示匹配所有字符，包括换行符
               r'</span>.*?<p class="">(?P<director>.*?)'
               r'&nbsp.*?主演: (?P<role>.*?)'
               r'<br>.*?(?P<year>.*?)&nbsp'
               r'.*?p;(?P<place>.*?)&nbsp.*?p;(?P<kind>.*?)</p>',re.S)   #re.S表示匹配所有字符，包括换行符
#提取数据
result=obj.finditer(page_content)

f=open("豆瓣网.csv","w",encoding="utf-8",newline="")

writer=csv.writer(f)

for item in result:
    dic=item.groupdict()     #将提取的数据以字典的形式存储
    dic["director"]=dic["director"].strip()  #去掉导演信息中的空格
    dic["year"]=dic["year"].strip()
    dic["place"]=dic["place"].strip()
    dic["kind"]=dic["kind"].strip()
    writer.writerow(dic.values()) #将词典的数据写入到csv文件中

f.close()    
print("写入完成~!")
