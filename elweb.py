import requests
from lxml import etree
import os
import codecs
from time import sleep


class Elweb:
    def __init__(self):
        self.requests = requests.Session()

    def __html_headers(self):
        headers = {
            'Host': 'elweb.elite-learning.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://eip.language-center.com.tw/',
            'Cookie': 'PHPSESSID=bl63ob0aqh9rik7nksrmhvrok6; _ga=GA1.3.1698690841.1642424111; _gid=GA1.3.371425795.1642424111; _gat_gtag_UA_149292473_2=1',
        }
        return headers

    def __video_headers(self):
        headers = {
            'Host': 'toefl-and-ielts.s3-ap-northeast-1.amazonaws.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Range': 'bytes=0-',
            'Referer': 'https://elweb.elite-learning.com.tw/',
        }
        return headers

    def __get_category(self):
        total_category_list = {}
        response = self.requests.get('https://elweb.elite-learning.com.tw/toefl_km/index.php?student_id=04111012001',
                                        headers = self.__html_headers()).text
        html = etree.HTML(response)
        categorys = html.xpath('//ul[@class="drop-down-menu"]/li')
        for category in categorys:
            small_category_list = []
            category_names = category.xpath('.//a/text()')
            category_urls = category.xpath('.//a/@href')
            for category_name, category_url in zip(category_names[1:], category_urls[1:]):
                current_url = f'https://elweb.elite-learning.com.tw/toefl_km/{category_url}'
                small_category_list.append({
                    'lesson':category_name,
                    'url':current_url
                })
            total_category_list[category_names[0]] = small_category_list
        
        return total_category_list
    
    def get_desktop(self):
        deskop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        return deskop_path
        
    def get_video_url(self, url):
        response = self.requests.get(url, headers=self.__html_headers()).text
        html = etree.HTML(response)
        url = html.xpath('//source/@src')
        return url[0]
    
    def crawl_video(self, path, name, url):
        response = self.requests.get(url, headers = self.__video_headers()).content
        print(response)
        with codecs.open(f'{path}/{name}.mp4', 'wb')as f:
            f.write(response)
    
    def main(self):
        categorys = self.__get_category()
        desktop = self.get_desktop()
        reversed_categorys = {}
        for k in reversed(list(categorys.keys())):
            reversed_categorys[k] = categorys[k]
        for dir_name, lesson in reversed_categorys.items():
            if not os.path.isdir(f'{desktop}/elweb/{dir_name}'):
                os.makedirs(f'{desktop}/elweb/{dir_name}')
            for information in lesson:
                video_name = information['lesson'].replace('/', '_')
                lesson_url = information['url']
                video_url = self.get_video_url(lesson_url)
                print(f'開始下載... {video_name}')
                self.crawl_video(f'{desktop}/elweb/{dir_name}', video_name, video_url)
                print(f'{video_name} 下載完成...')
                sleep(10) # 爬完一個影片，休息10秒  避免被發現
    

if __name__ == '__main__':
    Elweb().main()