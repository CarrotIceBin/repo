#1.找到未加密的参数
#2.把参数加密（参考网易云音乐的加密方式）   得到 params => encText 和 encSecKey=> encSecKey
#3.发送请求
import requests
import json
from base64 import b64encode
from Crypto.Cipher import AES
#目前已知参数
url="https://music.163.com/weapi/comment/resource/comments/get?csrf_token=cc5aec99fe7e2fb2d7b6659fc34f632f"
#请求方式 post

#这个就是未加密的参数 也是wyy根据网易云音乐的加密方式解密得到的原参数
data={
"csrf_token": "cc5aec99fe7e2fb2d7b6659fc34f632f",
"cursor": "-1",
"offset": "0",
"orderType": "1",
"pageNo": "1",
"pageSize": "20",
"rid": "R_SO_4_1430583016",
"threadId": "R_SO_4_1430583016"
}
#处理加密过程 
#函数调用传参
#window.asrsea(JSON.stringify(i0x), bse6Y(["流泪", "强"]), bse6Y(Qu1x.md), bse6Y(["爱心", "女孩", "惊恐", "大笑"]));
#参数说明：

#i0x: 未加密的参数即上面的data
#JSON.stringify(i0x): 将参数转换为json字符串形式

#bse6Y: 加密函数
#["流泪", "强"]:                  加密参数
#["爱心", "女孩", "惊恐", "大笑"]: 加密参数
#Quix.md:                         加密参数
i="YF4JW1bbfjVvGgOU"
f="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g="0CoJUm6Qyw8W8jud"
e="010001"

"""  window.asrsea的加密方式如下：


    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; d < a ; d += 1)
            e = Math.random() * b.length,  生成一个随机数
            e = Math.floor(e),             取整
            c += b.charAt(e);              取b中的随机字符
        return c                           返回一个长度为a的随机字符串
    }
    function b(a, b) { 
    
    c是密钥:密钥是一种特殊的字符串或数字序列，用于控制加密和解密过程。
        var c = CryptoJS.enc.Utf8.parse(b)                          
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)                          e是数据
          , f = CryptoJS.AES.encrypt(e, c, {           AES加密算法传入参数e数据,c是密钥,iv是初始化向量,mode是加密模式
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()                                   返回加密后的字符串
    }
    function c(a, b, c) {                 固定参数a返回同一个值 因为b,c是固定参数
        var d, e;                      
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {                d:data,e:'010001',f:很长,g:0CoJUm6Qyw8W8jud

        var h = {}                          h表示加密后的参数
        , i = a(16);                      i表示生成的随机字符串长度为16

        调用b函数加密encText,c函数加密encSecKey,并且将加密后的参数存入h中,返回h

        
        b进行了两次调用,第一次是把data和g传入生成encText文件,第二次是把encText文件和i传入生成encSecKey文件
        因此可推出b函数第一个参数是要加密的内容,第二个参数是随机字符串
        h.encText = b(d, g)                   g是密钥
        h.encText = b(h.encText, i)           返回的就是params

        h.encSecKey = c(i, e, f)              返回的就是encSecKey
        return h
    }

    window.asrsea = d; 

"""
#返回加密后的参数encSecKey
def get_encSecKey():
    return"2a6bed3bcc0e535b1140ac658c7e0e6233df98fc1ecfedf868faa8cfb7a5ff9eb154512b045d345a420cef8147465ad0cf6254104eff0564cec35e97b6b49864b513e4370ebe30534c913eeca80cf69037959e42a5fa6b6e6b2169c2e5428c42e64f2879ac4523b447965c7e09bfe35d5a81ce3d313a394cb131daeb266ed2ba"

#返回params
def get_params(data):
    first=get_encText(data,g)
    second=get_encText(first,i)
    return second    
#将bs的长度变为16的倍数
def to16(data):
    pad=16-len(data)%16
    data+=chr(pad)*pad
    return data
#返回加密后的参数encText
def get_encText(data,key):      #data要是bytestring类型
    iv="0102030405060708" 
    data=to16(data) 

    #key是bytes类型 iv是bytes类型
    aes=AES.new(key=key.encode('utf-8'),mode=AES.MODE_CBC,iv=iv.encode('utf-8'))  #创建加密器
    bs=aes.encrypt(data.encode('utf-8'))  #加密数据
    return str(b64encode(bs),'utf-8')

resp=requests.post(url,data={
    "params":get_params(json.dumps(data)),
    "encSecKey":get_encSecKey()
})

dic=resp.json()

commentsTitle=dic['data']['hotComments']

for comment in commentsTitle:
    print(comment['user']['nickname'],comment['timeStr'])
    print(comment['content'])