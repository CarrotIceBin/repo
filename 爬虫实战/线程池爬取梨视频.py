#1.找到需要爬取的视频的网址并保存视频
#2.使用多线程爬取所有视频
import requests
import time
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

def get_video_url():
    domain="https://www.pearvideo.com/"
#首先定位到需要爬取视频的主页面
    url="https://www.pearvideo.com/category_1"
    resp1=requests.get(url)
    resp1.encoding="utf-8"
    etree1=etree.HTML(resp1.text)
    rs1=etree1.xpath('//*[@id="categoryList"]/li')
    url_list=[]
    for i in rs1:
        video_url=i.xpath('div/a/@href')
        url_list.append(domain+video_url[0])
    return url_list
#注意防盗链 这里的referer一定要和domain一致 否则会403
def get_video_download(video_url):  

    id=video_url.split("_")[-1]

    headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Referer": video_url 
    }
    videoUrl=f"https://www.pearvideo.com/videoStatus.jsp?contId={id}&mrd=0.370733211366741"

    resp=requests.get(videoUrl,headers=headers)
    
    dic=resp.json()

    src=dic['videoInfo']['videos']['srcUrl']
    stime=dic['systemTime']

    #拿到视频原链接保存视频
    TrueUrl=src.replace(stime,f"cont-{id}")
    
    with open(r"D:\Code\video"+"\\"+id+".mp4", mode='wb') as f:
        f.write(requests.get(TrueUrl).content)
        
    print(f"视频{id}下载完成")
    f.close()
 

if __name__=='__main__':

    start_time = time.time()    
    url_list=get_video_url()
    with ThreadPoolExecutor(50) as executor:
         for url in url_list:
            executor.submit(get_video_download,url)

    # for url in url_list:
    #     get_video_download(url)
    end_time = time.time()
    print("总共耗时：", end_time - start_time)


    print("爬取完成")