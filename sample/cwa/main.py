import requests
from lxml import etree
import pandas as pd


class Cwa:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = self.__set_headers()
    
    def __set_headers(self):
        headers = {
            'Host': 'www.cwa.gov.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }
        return headers
        
    def get_country_info(self):
        output = {}
        response = self.requests.get(
            'https://www.cwa.gov.tw/Data/js/info/Info_County.js'
        )
        if response.status_code != 200:
            return None
        response_text = response.text
        country_list = self.filter_word(response_text)
        for country in country_list:
            country_id = country.get('ID')
            country_name = country.get('Name').get('C')
            output[country_id] = country_name
        return output  
        
    def get_town_info(self):
        output = {}
        response = self.requests.get(
            'https://www.cwa.gov.tw/Data/js/info/Info_Town.js'
        )
        if response.status_code != 200:
            return None
        response_text = response.text
        town_info_dict = self.filter_word(response_text)
        for country_id, town_list in town_info_dict.items():
            new_town_list = []
            for town in town_list:
                town_id = town.get('ID')
                town_name = town.get('Name').get('C')
                new_town_list.append({
                    'ID': town_id,
                    'Name': town_name
                })
            output[country_id] = new_town_list
        return output
    
    def filter_word(self, text:str):
        _text = text.replace('var Info_County =', '')
        _text = _text.replace('var Info_Town =', '')
        _text = _text.replace(';', '')
        _text = _text.replace('true', 'True')
        _text = _text.replace('false', 'False')
        _text = _text.replace('null', 'None')
        _text = eval(_text)
        return _text
            
    def get_country_mapping_code(self):
        output = {}
        country_dict = self.get_country_info()
        town_info_dict = self.get_town_info()
        for country_id, country_name in country_dict.items():
            town_list = town_info_dict.get(country_id)
            for town in town_list:
                town_id = town.get('ID')
                town_name = town.get('Name')
                output[f'{country_name}{town_name}'] = town_id
        return output
    
    def get_weather_response(self, code):
        output = []
        response = self.requests.get(
            f'https://www.cwa.gov.tw/V8/C/W/Town/MOD/Week/{code}_Week_PC.html'
        )
        if response.status_code != 200:
            return None
        timezone = ['早上', '晚上']
        tree = etree.HTML(response.text)
        weekday = self.get_week_day(tree)
        weather = self.get_weather(tree)
        high_temprature = self.get_high_temprature(tree)
        low_temprature = self.get_low_temprature(tree)
        rain_prob = self.get_rain_prob(tree)
        total_weeday = [f'{_weekday}{_time}' for _weekday in weekday for _time in timezone]
        for week_day, _weather, _high_temprature, _low_temprature, _rain_prob in zip(
            total_weeday, weather, high_temprature, low_temprature, rain_prob):
            output.append({
                '時間': f'{week_day}',
                '天氣': _weather,
                '最高溫度': _high_temprature,
                '最低溫度': _low_temprature,
                '降雨機率': _rain_prob
                
            })
        df = pd.DataFrame(output)
        return df
    
    def get_week_day(self, tree):
        _weekdays = tree.xpath('//thead//th[@headers]')
        _weekdays = [''.join(_weekday.xpath('.//text()')) for _weekday in _weekdays]
        return _weekdays
    
    def get_weather(self, tree):
        _weather = tree.xpath('//tbody/tr[2]//@title')
        return _weather
            
    def get_high_temprature(self, tree):
        _high_temprature = tree.xpath('//tbody/tr[3]/td/span[1]/text()')
        return _high_temprature
            
    def get_low_temprature(self, tree):
        _low_temprature = tree.xpath('//tbody/tr[4]/td/span[1]/text()')
        return _low_temprature
        
    def get_rain_prob(self, tree):
        _rain_prob = tree.xpath('//tbody/tr[5]/td/text()')
        return _rain_prob
    
    def __transfer(self, word):
        word = word.replace('台', '臺')
        return word
    
    def main(self, country):
        print(f'=================={country}==================')
        country = self.__transfer(country)
        mapping_code_dict = self.get_country_mapping_code()
        town_code = mapping_code_dict.get(country)
        if town_code:
            return self.get_weather_response(town_code)
        else:
            return f'{country}查無資料'


if __name__ == '__main__':
    obj = Cwa()
    # obj.get_country_info()
    # print(obj.get_town_info())
    print(obj.get_weather_response('6301000'))
    
