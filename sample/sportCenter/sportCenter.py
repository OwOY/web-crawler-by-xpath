import codecs
import requests
from lxml import etree
from datetime import datetime, timedelta
from time import sleep
from random import uniform


class SportCenter:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
        self.requests.headers['ASP.NET_SessionId'] = self.set_cookie()
        
    def __set_headers(self):
        headers = {
            'Host': 'scr.cyc.org.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://scr.cyc.org.tw/tp09.aspx?module=net_booking&files=booking_place&PT=1',
        }
        return headers
    
    def set_cookie(self):
        response = self.requests.get('https://scr.cyc.org.tw/tp09.aspx')
        if response.status_code == 200:
            sessionId = response.cookies.get('ASP.NET_SessionId')
        return sessionId
    
    def get_html_response(self, date:str):
        """取得球場狀態的html tree

        Args:\n
            date (str): 日期 ex:YYYY/MM/DD
        """
        response = self.requests.get(
            'https://scr.cyc.org.tw/tp09.aspx',
            params = {
                'module': 'net_booking',
                'files': 'booking_place',
                'StepFlag': '2',
                'PT': '1',
                'D': date,
                'D2': '3'
            }
        )
        return response
    
    def get_tree(self, response):
        tree = etree.HTML(response.text)
        return tree

    def get_login(self, client_id, password, captcha):
        self.requests.post(
            'https://scr.cyc.org.tw/tp09.aspx',
            params={
                'Module': 'login_page',
                'files': 'login'
            },
            data={
                'loginid': client_id,
                'loginpw':password,
                'Captcha_text': captcha
            }
        )
        
    def get_captcha(self):
        response = self.requests.get(
            'https://scr.cyc.org.tw/NewCaptcha.aspx'
        )
        with codecs.open('captcha.jpg', 'wb') as f:
            f.write(response.content)
    
    def get_court_status(self, tree):
        """取得球場狀態

        Args:\n
            tree (etree): html tree
        """
        order_court_dict = {}
        table_list = tree.xpath('//span[@id="ContentPlaceHolder1_Step2_data"]//tr')
        idx = 0
        for table in table_list[1:]:
            if idx%6 == 0:
                time = table.xpath('./td[1]/text()')
                court = table.xpath('./td[2]/text()')
                prize = table.xpath('./td[3]/text()')
                status = table.xpath('./td[4]/img/@onclick')
            else:
                court = table.xpath('./td[1]/text()')
                prize = table.xpath('./td[2]/text()')
                status = table.xpath('./td[3]/img/@onclick')
            idx += 1
            print(time[0], court[0], prize[0])
            if ('您是否確定預約' in status[0] and
                (time[0] == '18:00~19:00' or time[0] == '19:00~20:00')
            ):
                order_loc = status[0].split('Step3Action(')[1].split(',')
                if time[0] not in order_court_dict:
                    order_court_dict[time[0]] = order_loc
                print(time[0], court[0], prize[0], order_loc)
        return order_court_dict
    
    def order_court(self, str_dt, order_court_dict):
        """訂球場
        Args:
            order_court_dict (dict): key為日期，value為球場座標
        """
        for _, court in order_court_dict.items():
            x = court[0]
            y = court[1].split(')')[0]
            self.requests.get(
                'https://scr.cyc.org.tw/tp09.aspx',
                params={
                    'module': 'net_booking',
                    'files': 'booking_place',
                    'StepFlag': '25',
                    'QPid': x,
                    'QTime': y,
                    'PT': '1',
                    'D': str_dt
                }
            )
            sleep(0.1)
    
    def line_notify(self, line_token, msg):
        payload = {'message':msg}
        requests.post(
            'https://notify-api.line.me/api/notify',
            data=payload,
            headers={'Authorization':f'Bearer {line_token}'}
        )
    
    def read_config(self):
        config_dict = {}
        with codecs.open('password.ini', 'r') as f:
            config_list = f.readlines()
        for data in config_list:
            key, value = data.split('=')
            config_dict[key] = value.strip()
        return config_dict
    
    def main(self):
        """調整規律，因只開放搶下禮拜當日場地，固只搶下周四、五的場地
        """
        self.get_captcha()
        config_dict = self.read_config()
        client_id = config_dict.get('CLINET')
        password = config_dict.get('PASSWORD')
        line_token = config_dict.get('LINETOKEN')
        captcha = input('請輸入驗證碼:')
        self.get_login(client_id, password, captcha)
        
        while True:
            now_date = datetime.now()
            now_weekday = now_date.weekday()
            now_hour = now_date.hour
            now_minute = now_date.minute
            # 週三23:50~週四01:00
            # 週四23:50~週五01:00
            if (now_weekday != 3 
                and now_weekday != 4
            ):
                print(f'未到搶場地時間，等待中...{now_date}')
                sleep(60*60)
                continue
            sleep_time = 60
            if (
                (now_weekday == 2 and now_hour == 23 and now_minute > 59) or 
                ((now_weekday == 3 or now_weekday == 4) and now_hour < 1 )
            ):
                sleep_time = uniform(0.5, 1.3)
            
            next_week_date = now_date + timedelta(days=7)
            str_dt = next_week_date.strftime('%Y/%m/%d')
            print('查看日期:', str_dt)
            response = self.get_html_response(str_dt)
            tree = self.get_tree(response)
            order_court_dict = self.get_court_status(tree)
            if len(order_court_dict) == 2:
                print(f'已搶到場地{str_dt}')
                self.order_court(str_dt, order_court_dict)
                self.line_notify(line_token, f'{str_dt}已搶到場地')
                break
            sleep(sleep_time)
    
            
if __name__ == '__main__':
    sc = SportCenter()
    sc.main()
