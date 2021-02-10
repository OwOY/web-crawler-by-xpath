import requests
from lxml import etree
import prettytable as pt
import os

class New_amazing:

    def __init__(self):

        self.requests = requests.Session()
        self.main()


    def main(self):

        print('請輸入搜尋日期(xxxx/xx/xx)')
        begin_date = str(input('起 : '))
        end_date = str(input('迄 : '))
        self.get_trip_list(begin_date, end_date, 1)


    def get_tree(self, url):

        response = self.requests.get(url,headers = {
            'Host': 'www.4p.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'https://www.4p.com.tw',
            'Referer': 'https://www.4p.com.tw/EW/GO/GroupList.asp'
        }).text
        html = etree.HTML(response)
        return html


    def get_json(self, begin_date, end_date, page):

        response = self.requests.post('https://www.4p.com.tw/EW/Services/SearchListData.asp',headers = {
            'Host': 'www.4p.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'https://www.4p.com.tw',
            'Referer': 'https://www.4p.com.tw/EW/GO/GroupList.asp'
        },data = {
            'pageALL':page,
            'beginDt':begin_date,
            'endDt':end_date
        }).json()
        return response


    def get_trip_list(self, begin_date, end_date, page):
        
        tb = pt.PrettyTable(['ID', 'tour_name','leave_datetime','tourdate','Airport','Price','totalseat','leftseat','order_deadline'])
        datas = self.get_json(begin_date, end_date, page)
        ID = 1
        url_list = []
        for data in datas['All']:
            trip_ID = data['GrupCd']
            leave_datetime = data['LeavDt']
            tour_name = data['GrupSnm']
            tour_date = data['GrupLn']
            totalseat = data['EstmYqt']
            leftseat = data['SaleYqt']
            port_name = data['PortNm']
            order_deadline = data['OrderDl']
            price = data['SaleAm']
            url_list.append('https://www.4p.com.tw' + data['Url'])
            tb.add_row([ID, f'[{trip_ID}]{tour_name}', leave_datetime, tour_date, port_name, price, totalseat, leftseat, order_deadline])
            ID += 1        

        while True:
            print(tb)
            user_choose = int(input('請選擇動作(0)離開(1)查看資訊(2)上一頁(3)下一頁 : '))
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                choose_trip = int(input('請輸入要看的旅遊ID : '))
                self.get_info(url_list[choose_trip - 1])
            elif user_choose == 2:
                if page == 1:
                    print('已經是第1頁囉')
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                else:
                    page -= 1
                    self.get_trip_list(begin_date, end_date, page)
            elif user_choose == 3:
                page += 1
                self.get_trip_list(begin_date, end_date, page)
                

    def get_info(self, url):
        
        html = self.get_tree(url)
        day_title = html.xpath('//h4[@class="col-xs-12 col-sm-12 col-md-11 col-lg-11 day_title_right"]//text()')
        day_contents = html.xpath('//div[@class="col-xs-12 col-sm-12 col-md-12 col-lg-12 day_content"]')
        day_contents = [''.join(day_content.xpath('.//text()')) for day_content in day_contents]
        day_meals = html.xpath('//div[@class="meal_content"]')
        day_meals = ['\n'.join(day_meal.xpath('.//text()')).replace(' ','').replace('\r\n','').strip() for day_meal in day_meals]
        day_hotel = html.xpath('//p[@name="itnHtl"]//text()')
        i = 0
        print('==============================================================================')
        while True:
            try:
                print(f'Title:{day_title[i].strip()}\n\n旅遊描述:{day_contents[i].strip()}\n\n{day_meals[i].strip()}\n\nHotel:{day_hotel[i].strip()}')
            except:
                break
            i += 1
            print('==============================================================================')
        # os.system('pause')   #windows選擇使用
        os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用

if __name__ == '__main__':
    
    # Tourist4p().get_info('https://www.4p.com.tw/EW/GO/GroupDetail.asp?prodCd=TWNBR210223C')
    New_amazing()