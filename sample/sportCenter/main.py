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
    
    def order_court(self, str_dt):
        """訂球場
        Args: 
            str_dt(str):
        """
        court_list = ['83', '84', '1074', '1075', '87', '88']
        time_list = ['18', '19']
        for _time in time_list:
            for _court in court_list:
                self.requests.get(
                    'https://scr.cyc.org.tw/tp09.aspx',
                    params={
                        'module': 'net_booking',
                        'files': 'booking_place',
                        'StepFlag': '25',
                        'QPid': _court,
                        'QTime': _time,
                        'PT': '1',
                        'D': str_dt
                    }
                )
                sleep(0.1)
    
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
        captcha = input('請輸入驗證碼:')
        self.get_login(client_id, password, captcha)
        sleep_time = 60
        
        while True:
            now_date = datetime.now()
            now_weekday = now_date.weekday()
            now_hour = now_date.hour
            now_minute = now_date.minute
            # 週三23:50~週四01:00
            # 週四23:50~週五01:00
            if (
                (now_weekday == 2 and now_hour == 23 and now_minute > 59) or 
                (now_weekday == 3 and now_hour == 23 and now_minute > 59) or 
                ((now_weekday == 3 or now_weekday == 4) and now_hour < 1 and now_minute < 2)
            ):
                print('準備開搶...')
                sleep_time = uniform(0.1, 0.5)
                
                if now_minute == 0:
                    next_week_dt = now_date + timedelta(days=7)
                    next_week_str_dt = next_week_dt.strftime('%Y/%m/%d')
                    self.order_court(next_week_str_dt)
                    print('已搶完下周場地')
                    break
            else:
                print(f'未到搶場地時間，等待中...{now_date}')
                sleep(60*60)
                continue
            sleep(sleep_time)
            
if __name__ == '__main__':
    sc = SportCenter()
    sc.main()
