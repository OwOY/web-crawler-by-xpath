import requests
from lxml import etree
import prettytable as pt
import os

class Bwf:

    def __init__(self):
        self.requests = requests.Session()
        self.main()

    def main(self):
        
        value = self.get_new_value()
        while True:
            user_choose = int(input('請選擇要查看的項目(0)離開(1)男單(2)女單(3)男雙(4)女雙(5)混雙 : '))
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                self.get_men_single_rank(value)
            elif user_choose == 2:
                self.get_women_single_rank(value)
            elif user_choose == 3:
                self.get_mens_double_rank(value)
            elif user_choose == 4:
                self.get_womens_double_rank(value)
            elif user_choose == 5:
                self.get_mix_double_rank(value)
            else:
                print('請重新輸入')
            # os.system('pause')   #windows選擇使用
            os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用


    def get_tree(self, url):
        
        response = self.requests.get(url, headers = {
            'Host': 'bwf.tournamentsoftware.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://bwf.tournamentsoftware.com/ranking/'
        }).text
        html = etree.HTML(response)
        return html


    def get_new_value(self):

        html = self.get_tree('https://bwf.tournamentsoftware.com/ranking/ranking.aspx?rid=70')
        value = html.xpath('//select[@class="publication"]/option[1]/@value')[0]
        return value

    
    def get_men_single_rank(self, value):
        
        tb = pt.PrettyTable(['Rank','Country','player','point'])
        html = self.get_tree(f'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={value}&category=472')
        infos = html.xpath('//table[@class="ruler"]//tr')[2:-1]
        infos = [info.xpath('.//text()') for info in infos]
        for info in infos:
            rank = info[1]
            country = info[11]
            player = info[6]
            point = info[8]
            tb.add_row([rank, country, player, point])
        print(tb)


    def get_women_single_rank(self, value):
        
        tb = pt.PrettyTable(['Rank','Country','player','point'])
        html = self.get_tree(f'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={value}&category=473')
        infos = html.xpath('//table[@class="ruler"]//tr')[2:-1]
        infos = [info.xpath('.//text()') for info in infos]
        for info in infos:
            rank = info[1]
            country = info[11]
            player = info[6]
            point = info[8]
            tb.add_row([rank, country, player, point])
        print(tb)


    def get_mens_double_rank(self, value):
        
        tb = pt.PrettyTable(['Rank','Country','player1','player2','point'])
        html = self.get_tree(f'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={value}&category=474')
        infos = html.xpath('//table[@class="ruler"]//tr')[2:-1]
        infos = [info.xpath('.//text()') for info in infos]
        for info in infos:
            rank = info[1]
            country = info[15]
            player1 = info[7]
            player2 = info[9]
            point = info[12]
            tb.add_row([rank, country, player1, player2, point])
        print(tb)


    def get_womens_double_rank(self, value):
        
        tb = pt.PrettyTable(['Rank','Country','player1','player2','point'])
        html = self.get_tree(f'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={value}&category=475')
        infos = html.xpath('//table[@class="ruler"]//tr')[2:-1]
        infos = [info.xpath('.//text()') for info in infos]
        for info in infos:
            rank = info[1]
            country = info[15]
            player1 = info[7]
            player2 = info[9]
            point = info[12]
            tb.add_row([rank, country, player1, player2, point])
        print(tb)


    def get_mix_double_rank(self, value):
        
        tb = pt.PrettyTable(['Rank','Country','player1','player2','point'])
        html = self.get_tree(f'https://bwf.tournamentsoftware.com/ranking/category.aspx?id={value}&category=476')
        infos = html.xpath('//table[@class="ruler"]//tr')[2:-1]
        infos = [info.xpath('.//text()') for info in infos]
        for info in infos:
            rank = info[1]
            country = info[15]
            player1 = info[7]
            player2 = info[9]
            point = info[12]
            tb.add_row([rank, country, player1, player2, point])
        print(tb)

if __name__ == '__main__':
    
    Bwf()