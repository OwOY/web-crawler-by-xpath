import requests 
from lxml import etree
import codecs
import os


class CrawlCat:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        
    def __set_headers(self):
        headers = {
            'Host': 'store.line.me',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://store.line.me/stickershop/author/751898/zh-Hant'
        }
        return headers
    
    def get_main_page(self, page):
        response = self.requests.get(
            f'https://store.line.me/stickershop/author/751898/zh-Hant?page={page}',
        )
        if response.status_code == 200:
            return response
        return None
    
    def get_page_url(self, response):
        tree = etree.HTML(response.text)
        url_list = tree.xpath('//ul[@class="mdCMN02Ul"]/li/a/@href')
        url_list = [f'https://store.line.me{url}' for url in url_list]
        return url_list
    
    def get_image(self, url):
        response = self.requests.get(url)
        tree = etree.HTML(response.text)
        image_url_list = tree.xpath('//ul[@class="mdCMN09Ul FnStickerList"]//span[@class="mdCMN09Image"]/@style')
        image_url_list = [image.split('image:url(')[-1][:-2] for image in image_url_list]
        return image_url_list
    
    def download_image(self, image_name, image_url):
        response = self.requests.get(
            image_url,
            headers={
                'Host': 'stickershop.line-scdn.net',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
            }
        )
        if not os.path.isdir('cat'):
            os.makedirs('cat')
        with codecs.open(f'cat/{image_name}.png', 'wb')as f:
            f.write(response.content)
    
    def main(self):
        page = 1
        image_name = 0
        while True:
            response = self.get_main_page(page)
            if not response:
                break
            url_list = self.get_page_url(response)
            for url in url_list:
                image_url_list = self.get_image(url)
                for image_url in image_url_list:
                    self.download_image(image_name, image_url)
                    image_name += 1
            page += 1
            
            
if __name__ == '__main__':
    CrawlCat().main()
