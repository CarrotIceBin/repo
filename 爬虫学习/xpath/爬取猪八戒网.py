import requests
from lxml import etree

url ="https://www.zbj.com/fw/?k=SAAS"

resp=requests.get(url)
resp.encoding='utf-8'
html=etree.HTML(resp.text)
#获取所有商品div              
divs=html.xpath('//*[@id="__layout"]/div/div[3]/div[1]/div[4]/div/div[2]/div/div[2]/div')

#获取商品名称
for div in divs:
    name="assa".join(div.xpath('div/div[3]/div[2]/a/span/text()'))
    print(name)