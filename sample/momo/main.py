import requests
from datetime import datetime
import codecs
import os
from time import sleep


class MomoCrawl:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        self.idx = 0
        
    def __set_headers(self):
        headers = {
            'Host': 'apisearch.momoshop.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'https://www.momoshop.com.tw',
            'Referer': 'https://www.momoshop.com.tw/'
        }
        return headers
    
    def get_menu(self, category, page):
        now_timestamp = datetime.now().timestamp()
        payload = {
            "host": "momoshop",
            "flag": "searchEngine",
            "data": {
                "specialGoodsType": "",
                "isBrandSeriesPage": False,
                "authorNo": "",
                "originalCateCode": "",
                "cateType": "",
                "searchValue": category,
                "cateCode": "",
                "cateLevel": "-1",
                "cp": "N",
                "NAM": "N",
                "first": "N",
                "freeze": "N",
                "superstore": "N",
                "tvshop": "N",
                "china": "N",
                "tomorrow": "N",
                "stockYN": "N",
                "prefere": "N",
                "threeHours": "N",
                "video": "N",
                "cycle": "N",
                "cod": "N",
                "superstorePay": "N",
                "showType": "chessboardType",
                "curPage": page,
                "priceS": "0",
                "priceE": "9999999",
                "searchType": "1",
                "reduceKeyword": "",
                "isFuzzy": "0",
                "rtnCateDatainfo": {
                    "cateCode": "",
                    "cateLv": "-1",
                    "keyword": category,
                    "curPage": page,
                    "historyDoPush": True,
                    "timestamp": int(now_timestamp)
                },
                "flag": 2018,
                "serviceCode": "MT01",
                "addressSearchData": {},
                "adSource": "tenmax"
            }
        }
        response = self.requests.post(
            'https://apisearch.momoshop.com.tw/momoSearchCloud/moec/textSearch',
            json=payload
        )
        return response.json()
    
    def get_image(self, response_json):
        """取得商品圖片
        Args:
            response_json(dict):
        """
        for data in response_json.get('rtnSearchData').get('goodsInfoList'):
            img_url = data.get('imgUrl')
            self.download_image(img_url)

    def download_image(self, url):
        url = url.replace('.jpg', '.webp')
        domain = url.replace('https://', '').split('/')[0]
        response = self.requests.get(
            url,
            headers = {
                'Host': domain,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
            }
        )
        if response.status_code != 200:
            print(f'{url} Error')
            return 
        with codecs.open(f'img/{self.idx}.jpg', 'wb')as f:
            f.write(response.content)
        print(f'{url} 圖片下載完成')
        self.idx += 1
        
    def main(self, category):
        if not os.path.isdir('img'):
            os.mkdir('img')
        for page in range(1, 101):
            response_json = self.get_menu(category, page)
            self.get_image(response_json)
            sleep(0.3)


if __name__ == '__main__':
    obj = MomoCrawl()
    obj.main('餅乾')