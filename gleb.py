import requests
from lxml import etree
import os
import codecs
import re
from loguru import logger

###################################
# Maintain:David                  #
# Email:engineeryang01@gmail.com  #
###################################

class GlenCrawl:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        
    def __set_headers(self):
        headers = {
            'Host': 'glen-powell.org',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }
        return headers
    
    def get_category(self):
        """取得所有分類
        """
        response = self.requests.get('https://glen-powell.org/photos/')
        tree = etree.HTML(response.text)
        
        category_list = tree.xpath('//article//span[@class="catlink"]//text()')
        category_link_list = tree.xpath('//article//span[@class="catlink"]//@href')
        category_link_list = [f'https://glen-powell.org/photos/{category_link}'
                              for category_link in category_link_list]            
        return category_list, category_link_list
    
    def get_year_page(self, category_link):
        """取得所有年分

        Args:
            category_link (str): 分類連結

        """
        response = self.requests.get(category_link)
        tree = etree.HTML(response.text)
        year_list = tree.xpath('//article//span[@class="catlink"]//text()')
        year_link_list = tree.xpath('//article//span[@class="catlink"]//@href') # index.php?cat=70
        year_link_list = [f'https://glen-powell.org/photos/{year}'
                     for year in year_link_list]
        return year_list, year_link_list

    def get_album_link(self, year_link):
        """取得所有相簿連結

        Args:
            year_link (str): 年份網址

        """
        total_album_link = []
        total_album_title = []
        try:
            last_page = 1
            response = self.requests.get(year_link)
            tree = etree.HTML(response.text)
            other_page = tree.xpath('//td[@class="navmenu"]//text()')
            if other_page:
                last_page = other_page[-1]
            page = 1    
            while page <= int(last_page):
                response = self.requests.get(year_link,
                                            params = {'page':page})
                tree = etree.HTML(response.text)
                album_link_list = tree.xpath('//table[@class="maintable "]//span[@class="alblink"]//@href')
                album_title_list = tree.xpath('//table[@class="maintable "]//span[@class="alblink"]//text()')
                album_link_list = [f'https://glen-powell.org/photos/{album_link}'
                                for album_link in album_link_list]
                total_album_link += album_link_list
                total_album_title += album_title_list
                page +=1
        except Exception as error:
            logger.info(error)
            
        return total_album_title, total_album_link
    
    def get_pic_link_list(self, album_link):
        """取得所有圖片連結

        Args:
            album_link (str): 相簿連結
        """
        response = self.requests.get(album_link)
        tree = etree.HTML(response.text)
        pic_link_list = tree.xpath('//td[@class="thumbnails"]//@src')
        pic_link_list = [f'https://glen-powell.org/photos/{pic_link.replace("thumb_", "")}'
                         for pic_link in pic_link_list]
        return pic_link_list
        
    def download_img(self, download_dir, pic_link_list):
        """下載圖片

        Args:
            download_dir (str): 下載目錄
            pic_link_list (str): 圖片連結
        """
        pic_id = 1
        for pic_link in pic_link_list:
            response = self.requests.get(pic_link)
            with codecs.open(f'{download_dir}/{pic_id}.png', 'wb')as f:
                f.write(response.content)
            pic_id += 1
            
    def main(self):
        """主執行程式
        """
        category_list, category_link_list = self.get_category()
        for category, category_link in zip(category_list, category_link_list):
            year_list, year_link_list = self.get_year_page(category_link)
            
            for year, year_link in zip(year_list, year_link_list):
                album_title_list, album_link_list = self.get_album_link(year_link)
                
                for album_title, album_link in zip(album_title_list, album_link_list):
                    album_title = re.sub(r'[\/]', '', album_title)
                    download_dir = f'download/{category}/{year}/{album_title}'
                    download_dir = re.sub(r'[:*?"><|]', '', download_dir)
                    if not os.path.isdir(download_dir):
                        os.makedirs(download_dir)
                    pic_link_list = self.get_pic_link_list(album_link)
                    self.download_img(download_dir, pic_link_list)
                    print(f'{album_title} 下載完成')
            
if __name__ == '__main__':
    glen = GlenCrawl()
    glen.main()
    # print(glen.get_category())
    # print(glen.get_year_page('https://glen-powell.org/photos/index.php?cat=2'))
    # print(glen.get_album_link('https://glen-powell.org/photos/index.php?cat=66'))
    # print(glen.get_pic_link_list('https://glen-powell.org/photos/thumbnails.php?album=258'))