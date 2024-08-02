#导入自动化模块来处理解密过程 直接对数据进行抓取
from DrissionPage import ChromiumPage
from concurrent.futures import ThreadPoolExecutor
import re
import requests
import time
def get_video_url(dyer):
    domain="https://www.douyin.com/video/"
    dp=ChromiumPage()
    dp.listen.start('/post')
    dp.get(dyer)
    resp=dp.listen.wait()
    dp.close()
    ids=resp.response.body['aweme_list']
    urllist=[]
    for i in ids:
        urllist.append(domain+i['aweme_id'])
    return urllist
def get_video_download(url):
    obj=re.compile(r'http://v3-web.douyinvod.com/.*',re.S)
    id=url.split('/')[-1]
    dp=ChromiumPage()
    dp.listen.start('/detail')
    dp.get(url)
    resp=dp.listen.wait()
    dp.close()
    title=resp.response.body['aweme_detail']['desc']
    srcurls=resp.response.body['aweme_detail']['video']['play_addr']['url_list']
    for i in srcurls:
        url=obj.findall(i)
        if url:
            srcurl=url[0]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "Referer":"https://www.douyin.com/"
    }
    #二进制编写来保存mp4文件D:\Code\video
    resp=requests.get(srcurl,headers=headers)
    content=resp.content
    with open(r"D:\Code\video"+"\\"+id+".mp4",mode='wb') as f:
        f.write(content)    
    print(title+" 已下载完毕即将进入下一个视频") 
if __name__ == '__main__':
    st=time.time()
    dyer=input("请输入抖音用户主页链接："+"\n")
    print("正在获取视频链接中")
    #dyer="https://www.douyin.com/user/MS4wLjABAAAA94jVX_OnV2mc6BBiYj3Y4RBklTiselvG7yRZJa3Aarw"
    url_list=get_video_url(dyer)
    print("视频链接获取完毕，准备下载")
    with ThreadPoolExecutor(50) as f:  
        for url in url_list:
            f.submit(get_video_download(url))
  
    ed=time.time()
    print(ed-st,"秒")

    print("所有视频下载完毕！")