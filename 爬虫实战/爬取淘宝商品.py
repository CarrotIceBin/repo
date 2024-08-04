import json
import re
from pprint import pprint
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage
import requests
# def get_shop_url(url):
#     domain='https://item.taobao.com'
#     # url_list = []
#     # dp = ChromiumPage()
#     # dp.listen.start('/2.0')
#     # dp.get(url)
#     # resp = dp.listen.wait()
#     # dp.close()

#     # dic=resp.response.body

#     # js=dic.replace("mtopjsonp3","")
#     # jso=json.dumps(js,ensure_ascii=False)
#     # json_data = json.loads(jso)
#     #print(jso)

#     with open('shop_url.json', 'r', encoding='utf-8') as f:
#         json_str = f.read()
#         json_data = json.loads(json_str)
#         info=json_data['data']['itemsArray']
#         for i in info:
#             title=i['shopInfo']['title']
#             price=i['price']
#             url=i['auctionURL']
#             print(title,price,url)
#     #print(json_data)


# if __name__ == '__main__':
#     shop_url = get_shop_url("https://s.taobao.com/search?_input_charset=utf-8&commend=all&ie=utf8&initiative_id=tbindexz_20170306&localImgKey=&page=1&q=%E9%A9%AC%E6%9D%A5%E6%9C%8D%E4%BB%A3%E5%85%85%E7%93%A6%E7%BD%97%E5%85%B0%E7%89%B9&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.201856.d13&ssid=s5-e&suggest=history_1&suggest_query=&tab=all&wq=")


resp=requests.get(url="https://item.taobao.com/item.htm?id=750753164587&ns=1&abbucket=3#detail&xxc=taobaoSearch")

print(resp.text)