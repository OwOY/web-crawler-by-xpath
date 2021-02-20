import requests
from lxml import etree
import prettytable as pt
import os

class Weather:
    
    def __init__(self, ):
        
        self.requests = requests.Session()
        
        
    # def main(self):


    def get_tree(self, url):
        
        response = self.requests.get(url, headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Host':'www.cwb.gov.tw',
            'Referer':'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=65',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
        }).text
        html = etree.HTML(response)
        return html

    def get_location_ID(self):
        
        tb = pt.PrettyTable(['ID','CID','location'])
        html = self.get_tree('https://www.cwb.gov.tw/V8/C/W/County/index.html')
        CID = html.xpath('//g/@id')
        location = html.xpath('//g/desc/text()')
        i = 1
        CID_list = []
        while i < len(CID):
            tb.add_row([i, CID[i].replace('C',''), location[i]])
            CID_list.append(CID[i].replace('C',''))
            i += 1
        print(tb)
        self.user_choose_location(CID_list)

    def user_choose_location(self, CID_list):
        
        user_choose = int(input('請選擇要察看的地點或是按(0)離開 : '))

        if user_choose == 0:
            os._exit(0)
        else:
            try:
                self.get_week_temp(CID_list[user_choose - 1])
            except:
                print('請重新輸入')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                self.get_location_ID()


    def get_week_temp(self, CID):
        
        html = self.get_tree(f'https://www.cwb.gov.tw/V8/C/W/County/MOD/Week/{CID}_Week_PC.html?T=2021021018-3')
        describe_list = html.xpath('//th/text()')[1:-4]
        temp = html.xpath('//p[@class="text-center"]/span[@class="tem-C is-active"]/text()')
        temp_day = ['日溫'] + temp[:7]
        temp_night = ['夜溫'] + temp[7:]
        body_temp = html.xpath('//tr[@id="lo-temp"]/td/span[@class="tem-C is-active"]/text()')
        body_temp = ['體感溫度'] + body_temp
        ultra = html.xpath('//tr[@id="ultra"]/td/span[@class="sr-only"]/text()')
        ultra = ['紫外線'] + ultra
        day_list = ['日期']

        for i in range(0, len(describe_list), 2):
            day_list.append(describe_list[i]+describe_list[i+1])
        tb = pt.PrettyTable(day_list)
        tb.add_row(temp_day)
        tb.add_row(temp_night)
        tb.add_row(body_temp)
        tb.add_row(ultra)
        print(tb)

if __name__ == '__main__':
    
    Weather().get_location_ID()