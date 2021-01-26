import requests
from lxml import etree
import json
import time
import random
import prettytable as pt


class udn_news:

    def __init__(self):
        
        self.requests = requests.Session()
        self.main()
    

    def main(self):
        
        self.get_news()
        

    def get_html(self, page):
                
        h = {
                    'Host': 'udn.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'https://udn.com/news/breaknews/1',
                    'DNT': '1',
                    'Connection': 'keep-alive'
        }
        
        resp = requests.get(
            'https://udn.com/api/more?page=2&id=&channelId=1&cate_id=0&type=breaknews&totalRecNo=8198',
            headers = h,
            params = {
                'page':page,
                'id':'',
                'channelId':'1',
                'cate_id':'0',
                'type':'breaknews',
                'totalRecNo':'8198'
            }
        ).json()
        
        return resp
    

    def get_news(self):   
         
        for page in range(1,50):
            tb = pt.PrettyTable(['Title','Date','Link'])
            rest = random.randint(1,5)
            
            resp = self.get_html(page)
            a = resp['lists']
            for b in a:
                tb.add_row([b['title'], b['time']['date'], 'https://udn.com'+b['titleLink']])
            print(tb)
            time.sleep(rest)
            
            
if __name__ == '__main__':
    udn_news()
