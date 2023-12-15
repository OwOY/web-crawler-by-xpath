import requests
import os
import codecs
from dotenv import load_dotenv


load_dotenv()
class Feastogether:
    def __init__(self, meal_date, meal_time, meal_adult_ppl:int, meal_child_ppl:int):
        self.meal_date = meal_date
        self.meal_time = meal_time
        self.meal_adult_ppl = meal_adult_ppl
        self.meal_child_ppl = meal_child_ppl
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        self.set_token()
    
    def __set_headers(self):
        headers = {
            'Host': 'www.feastogether.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'application/json',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'https://www.feastogether.com.tw',
            'Referer': 'https://www.feastogether.com.tw/booking/Sunrise/process',
            'Sec-GPC': '1',
            'content-type': 'application/json',
            'language-locale': 'zh-tw'
        }
        return headers
    
    def set_token(self):
        act = os.getenv('act')
        payload = {
            "act":act,
            "pwd":os.getenv('psw'),
            "iCode":"+886",
            "countryCode":"TW",
            "memberAccessToken":""
        }
        response = self.requests.post(
            'https://www.feastogether.com.tw/api/994f5388-d001-4ca4-a7b1-72750d4211cf/custSignIn',
            json = payload,
        ).json()
        token = response.get('result').get('customerLoginResp').get('token')
        self.requests.headers['authorization'] = f'Bearer {token}'
        self.requests.headers['act'] = act
    
    def get_svg(self):
        payload = {"brandId":"BR00008"}
        response = self.requests.post(
            'https://www.feastogether.com.tw/api/994f5388-d001-4ca4-a7b1-72750d4211cf/get2FASvgByBrand',
            json = payload
        ).json()
        status_code = response.get('statusCode')
        if status_code == 1000:
            svg_code = response.get('result').get('code')
            svg_url = response.get('result').get('svg')
            with codecs.open('captcha.svg', 'w', encoding='utf-8') as f:
                f.write(svg_url)
            return svg_code
    
    def order(self, svg_code, svg_word):
        payload = {
            "storeId":"S2310060001",
            "peopleCount":self.meal_adult_ppl+self.meal_child_ppl,
            "mealPeriod":"lunch",
            "mealSeq":1,
            "mealDate":self.meal_date, # order_date
            "mealTime":self.meal_time, # order_time
            "zked":"1j6ul4y94ejru6xk7vu4vu4", # ??
            "svgCode":svg_code,
            "scgVerifyStr":svg_word # 驗證馬
        }
        response = self.requests.post(
            'https://www.feastogether.com.tw/api/booking/saveSeats',
            json = payload
        )
        print(response.json())
        
    def book(self):
        payload = {
            "brandName":"旭集",
            "storeName":"中茂店",
            "storeId":"S2310060001",
            "mealDate":self.meal_date,
            "mealPurpose":"",
            "mealSeq":1,
            "mealTime":self.meal_time,
            "mealPeriod":"lunch",
            "special":0,
            "childSeat":0,
            "adult":self.meal_adult_ppl,
            "child":self.meal_child_ppl,
            "chargeList":[
                {"seq":201,"count":self.meal_adult_ppl},
                {"seq":202,"count":self.meal_child_ppl}
            ],
            "storeCode":"XTWO",
            "bonusInfo":[],
            "yuuu":"892389djdj883831445",
            "redirectType":"iEat_card",
            "domain":"https://www.feastogether.com.tw",
            "pathFir":"booking",
            "pathSec":"result"
        }
        response = self.requests.post(
            'https://www.feastogether.com.tw/api/booking/booking',
            json = payload
        )
        print(response.status_code)
        print(response.text)
        
    def main(self):
        svg_code = self.get_svg()
        svg_word = input('請輸入驗證碼: ')
        self.order(svg_code, svg_word)
        self.book()
        

if __name__ == '__main__':
    meal_date = input('請輸入訂餐日期: ')
    meal_time = input('請輸入訂餐時間: ')
    meal_adult_ppl = int(input('請輸入訂餐人數(成人): '))
    meal_child_ppl = int(input('請輸入訂餐人數(小孩): '))
    obj = Feastogether(meal_date, meal_time, meal_adult_ppl, meal_child_ppl)
    obj.main()