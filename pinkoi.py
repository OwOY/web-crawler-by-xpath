import requests
from lxml import etree
from time import sleep
import pandas as pd
import threading
import codecs
import os
from loguru import logger

##############################
# Devlop:David               #
# Email:engineer01@gmail.com #
##############################

class Pinkoi:
    def __init__(self, csv_name):
        self.csv_name = f'{csv_name}.csv'
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        self.lock = threading.Lock()
        self.check_csv()
        
    def check_csv(self):
        if not os.path.isfile(self.csv_name):
            pd.DataFrame(columns=['標題', '價格', '敘述'])\
                .to_csv('camera.csv', index=False)
            
    def __set_headers(self):
        headers = {
            'Host': 'www.pinkoi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }
        return headers
    
    def __set_pic_headers(self):
        headers = {
            'Host': 'cdn01.pinkoi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'image/avif,image/webp,*/*',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }
        return headers
    
    def get_main_page(self, page):
        """抓取主頁面
        """
        params = {
            'owner':'rickphoto',
            'is_shop_page':'1',
            'sortby':'custom',
            'limit':'60',
            'page':page,
            'category':'11',
            'subcategory':'1110',
        }
        response_json = self.requests.get('https://www.pinkoi.com/apiv2/item/get_cards',
                                            params = params).json()
        return response_json['result']

    @logger.catch
    def get_detail(self, title, camera_id):
        """抓取相機頁面資料
        """
        response = self.requests.get(f'https://www.pinkoi.com/product/{camera_id}')
        tree = etree.HTML(response.text)
        desciption = tree.xpath('//div[@data-translate="description"]/text()')
        price = tree.xpath('//meta[@property="product:price:amount"]/@content')
        self.lock.acquire()
        self.write_to_csv(title, desciption[0], price[0])
        self.lock.release()
        
    def write_to_csv(self, title, desciption, price):
        """寫入csv
        """
        print(f'{title} 寫入完成')
        df = pd.DataFrame([{'標題':title,
                            '敘述':desciption,
                            '價格':price}])
        df.to_csv(self.csv_name, mode='a', index=False, header=False)
        
    def download_pic(self, title, camera_id):
        pic_id = 0
        file_dir = f'img/{title}'
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        while True:
            response = self.requests.get(f'https://cdn01.pinkoi.com/product/{camera_id}/{pic_id}/800x0.jpg',
                                         headers = self.__set_pic_headers())
            if response.status_code == 403:
                break
            with codecs.open(f'{file_dir}/{pic_id}.png', 'wb')as f:
                f.write(response.content)
            pic_id += 1
            sleep(0.1)
        
    # def main(self):
    #     """主要執行程式(執行速度快，但有lost資料風險)
    #     """
    #     page = 1
    #     detail_task_list = []
    #     download_pic_task_list = []
    #     while True:
    #         data_list = self.get_main_page(page)
    #         if not data_list:
    #             print('爬蟲結束')
    #             break
    #         for data in data_list:
    #             title = data['title']
    #             camera_id = data['tid']
    #             detail_task = threading.Thread(
    #                 target=self.get_detail, args=(title, camera_id))
    #             download_pic_task = threading.Thread(
    #                 target=self.download_pic, args=(title, camera_id))
                
    #             detail_task.start()
    #             detail_task_list.append(detail_task)
    #             download_pic_task.start()
    #             download_pic_task_list.append(download_pic_task)
    #         # 為了使請求不要過多且保障資料安全，每一隻API結束再請求下一隻    
    #         for detail_task in detail_task_list:
    #             detail_task.join()
    #         for download_pic_task in download_pic_task_list:
    #             download_pic_task.join()
                
    #         page += 1        
    #         sleep(1)
            
    def main(self):
        """主要執行程式
        """
        page = 1
        while True:
            data_list = self.get_main_page(page)
            if not data_list:
                print('爬蟲結束')
                break
            for data in data_list:
                title = data['title']
                camera_id = data['tid']
                detail_task = threading.Thread(
                    target=self.get_detail, args=(title, camera_id))
                download_pic_task = threading.Thread(
                    target=self.download_pic, args=(title, camera_id))
                
                detail_task.start()
                download_pic_task.start()
                # 為了使請求不要過多且保障資料安全，每一隻API結束再請求下一隻    
                detail_task.join()
                download_pic_task.join()
                
            page += 1        
            sleep(1)
            
        
if __name__ == '__main__':
    csv_name = str(input('請輸入想要的Excel名稱(不須加副檔名):'))
    pinkoi = Pinkoi(csv_name)
    pinkoi.main()