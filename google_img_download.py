import requests
from lxml import etree
import codecs
import json
import os
import random
import time

class google_img_download:

    def __init__(self):
        self.path = os.getcwd()
        self.requests = requests.Session()
        self.main()
        

    def main(self):
        
        num = 20
        i = 0

        want_img = str(input('請輸入想要下載的關鍵字：'))

        while True:
            
            rest = random.randint(1,5)
            
            dir_name = 'GoogleDownload'
            html = self.get_html(want_img, num)
            img_links = html.xpath('//img[@class="t0fcAb"]//@src')
            for img_link in img_links:
                if not os.path.isdir(dir_name):
                    os.mkdir(dir_name)
                    print(self.path+'\{0}資料夾創建完成'.format(dir_name))
                self.download_img(want_img, img_link, i)
                i+=1
            num += 20
            time.sleep(rest)
            

    def get_html(self, want_img, num):
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
        resp = requests.get(
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
        ).text
        html = etree.HTML(resp)
        return html
    

    def download_img(self, want_img, img_url, i):
        
        img = self.requests.get(img_url)
        with codecs.open(f'GoogleDownload/{want_img}{str(i)}.jpg','wb')as f:
            f.write(img.content)
            print(f'{want_img}{i} Done')
    
    
if __name__ == '__main__':
    
    google_img_download()
