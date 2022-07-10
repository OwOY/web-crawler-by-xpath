import requests
from lxml import etree
from region import RegionMap
from time import sleep
import threading


regionMap = RegionMap()
class RoadMap:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        self.task_list = []
        
    def __set_headers(self):
        headers = {
            'Host': 'zip5.5432.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }
        return headers
    
    def get_road(self, city, location_dict):
        response = self.requests.post(f'https://zip5.5432.tw/cityzip/新北市/{city}')
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        road_list = html.xpath('//table//a//text()')
        location_dict[city] = road_list
        
    def main(self):
        location_dict = {}
        city_list = regionMap.get_city()
        for city in city_list:
            task = threading.Thread(target=self.get_road, args=(city, location_dict))
            task.start()
            self.task_list.append(task)
            sleep(0.1)
        
        for task in self.task_list:
            task.join()
        
        return location_dict
            
if __name__ == '__main__':
    road = RoadMap()
    location_dict = road.main()
    print(location_dict)
    
        