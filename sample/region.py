import requests
from lxml import etree

class RegionMap:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        
    def __set_headers(self):
        headers = {
            'Host': 'sheethub.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.google.com/',
        }
        return headers
    
    def get_city(self):
        response = self.requests.get('https://sheethub.com/ronnywang/100年全國鄉鎮市區界圖/i/148/新北市')
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        region_list = html.xpath('//div[@class="panel-body"]/a/text()') 
        return region_list
        

if __name__ == '__main__':
    regionMap = RegionMap()
    regionMap.get_city()