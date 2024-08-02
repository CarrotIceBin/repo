import requests
from bs4 import BeautifulSoup
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
for ii in range(1,6):

    url="http://www.umeituku.com/bizhitupian/"+str(ii)+'.htm'

    res=requests.get(url,headers=headers)
    res.encoding="utf-8"

    soup=BeautifulSoup(res.text,"html.parser")  #把源代码交给BeautifulSoup解析器

    rs1=soup.find("div",attrs={"class":"TypeList"})

    rs_list=rs1.find_all("a")      #找到所有a标签

    print("第"+str(ii)+"页!!!")
    
    for i in rs_list: 
        url1=i.get("href")    #获取a标签的href属性值

        res2=requests.get(url1,headers=headers)  
        res2.encoding="utf-8"
        soup2=BeautifulSoup(res2.text,"html.parser")
        rs2=soup2.find("p",attrs={"align":"center"})   #找到图片所有的p标签

        src=rs2.get("src")   #获取图片的src属性值     
        #下载图片
        res3=requests.get(src,headers=headers)
        print(res3.status_code)
        #以/作为分隔符，把url的最后一部分 [-1] 作为文件名
        img_name=src.split("/")[-1]

        #res3.content 图片的二进制内容
        #以wb模式写入图片并保存到img文件夹下
        with open(r"D:\Code\爬虫\bs4\img"+"\\"+img_name,mode="wb") as f:
            f.write(res3.content)

        print("正在下载第"+str(ii)+"页第"+str(rs_list.index(i)+1)+"张图片:"+img_name)
        time.sleep(1)   #设置延时，防止被网站识别为爬虫


print("全部图片下载完成!") 

