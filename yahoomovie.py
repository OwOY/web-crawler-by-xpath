import requests
from lxml import etree
import prettytable as pt
import datetime
import os


def get_html(url, month):
    
    requests_session = requests.Session()
    resp = requests_session.get(
        url,
        headers = {
            'Host': 'movies.yahoo.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': 'XSRF-TOKEN=eyJpdiI6ImlLeElpRm9ScXlpSFU5RGdoUFpQRkE9PSIsInZhbHVlIjoiQU5CejFvcnA1bm1ZMlNGYWNLQ1FjdHl4UmRPM3BKRGd3aGNEZGNQUHQ5WkJQdE1YakVzc0t5RjBxc2V1eGFoTXducDYwcVwvZGdnMzl3NzhBb0o0emp3PT0iLCJtYWMiOiJmYzc5MWNlODYzODIyNDMzODY3NjZkZGI2ZWFiMTU4OWNjODY3OGY0MmYzMjY2ZmZmNTdlODU2M2NkYzM3ZmMzIn0%3D; ms55=eyJpdiI6ImxON0RHdnZDelgwdlV6RHF5YWtSQnc9PSIsInZhbHVlIjoicGFGXC9QcjVDVTg1SEF5YUZteGFaQmlDYXhoZ09aN1dtV0p5dUlPSWpSd1l6ZWlxQ2FwbWtKR2d3Qnl5STVOK3FDemxXZUtYOTJ0cjZOeFlXa1czd1VnPT0iLCJtYWMiOiIzMjUzMGNlMGY5NzY5ODIyMTlhZDkyOTFlYjY1MTBiYjY4YzNlMjQ0MjYwMTRjMTQ2OGVjYjVjNDc2MjU1ZDE4In0%3D; A1=d=AQABBPQQKV8CEMIP9Wg1wes3SeyKWQPRq9gFEgEBAQFiKl8yXwAAAAAA_SMAAAcI9BApXwPRq9g&S=AQAAAtqeX6NkBw2bDdn3Yb5PkPk; A3=d=AQABBPQQKV8CEMIP9Wg1wes3SeyKWQPRq9gFEgEBAQFiKl8yXwAAAAAA_SMAAAcI9BApXwPRq9g&S=AQAAAtqeX6NkBw2bDdn3Yb5PkPk; A1S=d=AQABBPQQKV8CEMIP9Wg1wes3SeyKWQPRq9gFEgEBAQFiKl8yXwAAAAAA_SMAAAcI9BApXwPRq9g&S=AQAAAtqeX6NkBw2bDdn3Yb5PkPk&j=WORLD; BX=dhauh0dfii47k&b=3&s=br; GUC=AQEBAQFfKmJfMkIiLASt; rxx=ps27djopeh.20nc97on&v=1; cmp=t=1596526836&j=0',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        },
        params = {
            'month':month
        }
    )
    resp.encoding = 'utf8'

    html = etree.HTML(resp.text)
    return html



def get_movie_info():
    
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    tb = pt.PrettyTable(['電影名稱','上映日期','網友期待度'])
    Total_Movie_Name = []
    Total_Release = []
    Total_expect = []



    print(f'{year}年電影上映資訊')
    while month < 13:
        
        html = get_html('https://movies.yahoo.com.tw/movie_comingsoon.html', month)
        # ---------------------------------------------------------------------------
        Movie_Name = html.xpath('//div[@class="release_movie_name"]')
        Movie_Name = [''.join(MN.xpath('.//a[@class="gabtn"]//text()')).replace(' ','').replace('\n','') for MN in Movie_Name]
        for MN in Movie_Name:
            Total_Movie_Name.append(MN)
        # ---------------------------------------------------------------------------
        expect = html.xpath('//dl[@class="levelbox"]')
        expect = [''.join(ep.xpath('.//div[1]//text()|.//span//text()')) for ep in expect]
        for ep in expect:
            Total_expect.append(ep)
        # ---------------------------------------------------------------------------
        Release_Movie_Time = html.xpath('//div[@class="release_movie_time"]//text()')
        for RMT in Release_Movie_Time:
            Total_Release.append(RMT)
        # ---------------------------------------------------------------------------
        month += 1
        
    for a,b,c in zip(Total_Movie_Name, Total_Release, Total_expect):
        tb.add_row([a,b,c])
    print(tb)


if __name__ == '__main__':
    
    get_movie_info()
