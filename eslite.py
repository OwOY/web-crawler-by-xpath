import requests
from lxml import etree
import time
import prettytable as pt
import random

tb = pt.PrettyTable(['Name','Date','Price','Price_cost'])

Book = str(input('請選擇要搜尋的書名 : '))


requests = requests.Session()

for page in range(1,5):
    rest = random.randint(1,5)
    p = requests.get(
        'http://www.eslite.com/Search_BW.aspx',
        headers = {
            'Host': 'www.eslite.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        },
        params = {
            'query': Book,
            'searchType': '',
            'page': page
        }
    )

    HTML = etree.HTML(p.text)

    BookName = HTML.xpath('//h3//span//text()')
    BookName = [B for B in BookName[1:]]

    Date = HTML.xpath('//td//span[2]//a//text()')

    Price = HTML.xpath('//td//span[5]')
    Price = [''.join(P.xpath('.//text()')).replace(' ','').replace('\r\n','').replace(',','') for P in Price]
    Price = [P if P != '' else '原價' for P in Price]

    Price_cost = HTML.xpath('//td//span[6]')
    Price_cost = [''.join(PC.xpath('.//text()')) for PC in Price_cost]
    time.sleep(rest)
    
    for a,b,c,d in zip(BookName, Date, Price, Price_cost):
        tb.add_row([a, b, c, d])
print(tb)
