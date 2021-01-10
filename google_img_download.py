import requests
from lxml import etree
import codecs
import json
import os
import random
import time

path = os.getcwd()

requests = requests.Session()

h = {
        'Host': 'www.google.com.tw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

num = 20
i = 0

want_img = str(input('請輸入想要下載的關鍵字：'))

while True:
    rest = random.randint(1,5)
    p = requests.get(
        'https://www.google.com.tw/search',
        headers = h,
        params = {
            'q':want_img,
            'hl':'zh-TW',
            'gbv':'1',
            'tbm':'isch',
            'ei':'nxoVX939NsmbmAXBzaKgAQ',
            'start':num,
            'sa':'N'
        }
    )
    dir_name = 'GoogleDownload'
    HTML = etree.HTML(p.text)
    img_Link = HTML.xpath('//img[@class="t0fcAb"]//@src')
    for img in img_Link:
        p1 = requests.get(img)
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
            print(path+'\{0}資料夾創建完成'.format(dir_name))
        with codecs.open('GoogleDownload/'+want_img+str(i)+'.jpg','wb')as f:
            f.write(p1.content)
            print('{0}{1} Done'.format(want_img,i))
        i+=1
    num += 20
    time.sleep(rest)