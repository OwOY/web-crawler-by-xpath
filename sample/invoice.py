import requests
from lxml import etree
from datetime import datetime
import os

class Invoice:
    
    def __init__(self, url):
        
        self.requests = requests.Session()
        self.url = url
        self.main()


    def main(self):

        print('''
兌獎規則
特別獎:同期統一發票收執聯8位數號碼與特別獎號碼相同者獎金1,000萬元
特獎:同期統一發票收執聯8位數號碼與特獎號碼相同者獎金200萬元
頭獎:同期統一發票收執聯8位數號碼與頭獎號碼相同者獎金20萬元
二獎:同期統一發票收執聯末7 位數號碼與頭獎中獎號碼末7 位相同者各得獎金4萬元
三獎:同期統一發票收執聯末6 位數號碼與頭獎中獎號碼末6 位相同者各得獎金1萬元
四獎:同期統一發票收執聯末5 位數號碼與頭獎中獎號碼末5 位相同者各得獎金4千元
五獎:同期統一發票收執聯末4 位數號碼與頭獎中獎號碼末4 位相同者各得獎金1千元
六獎:同期統一發票收執聯末3 位數號碼與 頭獎中獎號碼末3 位相同者各得獎金2百元
增開六獎:同期統一發票收執聯末3位數號碼與增開六獎號碼相同者各得獎金2百元
            ''')
        invoice_num = self.get_invoice_num()

        while True:

            your_invoice_num = str(input('請輸入你的發票號碼(共8碼)或輸入0離開 : '))
            if len(your_invoice_num) == 8:
                print(f'你的發票號碼為 : {your_invoice_num}')
            elif your_invoice_num == '0':
                break
            else:
                print('輸入錯誤，請重新輸入')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                continue

            print(self.check_winning(your_invoice_num, invoice_num))


    def get_tree(self):
        
        response = self.requests.get(self.url,
        headers = {
            'Host': 'invoice.etax.nat.gov.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        })
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)

        return html
    

    def get_invoice_num(self):
        
        html = self.get_tree()
        invoice_num = html.xpath('//div[@id="area1"]//span[@class="t18Red"]//text()')
        invoice_month = html.xpath('//div[@id="area1"]/h2[2]/text()')
        print(f'''
{invoice_month[0]}\n特別獎:{invoice_num[0]}\n特獎:{invoice_num[1]}\n\
頭獎 :{invoice_num[2]}\n增加6獎 :{invoice_num[3]}\n
---------------------------------------------------------------------------
                 ''')
        return invoice_num


    def check_winning(self, your_invoice_num, invoice_num):
        
        head_prize_list = invoice_num[2].split('、')
        six_prize_list = invoice_num[3].split('、')
        if your_invoice_num == invoice_num[0]:
            return('恭喜你中了特別獎！')
        if your_invoice_num == invoice_num[1]:
            return('恭喜你中了特獎！')

        for head_prize in head_prize_list:
            if your_invoice_num == head_prize:
                return('恭喜你中了頭獎！')
            elif your_invoice_num[1:] == head_prize[1:]:
                return('恭喜你中了二獎！')
            elif your_invoice_num[2:] == head_prize[2:]:
                return('恭喜你中了三獎！')
            elif your_invoice_num[3:] == head_prize[3:]:
                return('恭喜你中了四獎！')
            elif your_invoice_num[4:] == head_prize[4:]:
                return('恭喜你中了五獎！')
            elif your_invoice_num[5:] == head_prize[5:]:
                return('恭喜你中了六獎！')

        for six_prize in six_prize_list:
            if your_invoice_num[5:] == six_prize:
                return '恭喜你中了六獎！'

        return '沒中獎哦QQ'


if __name__ == '__main__':
    
    Invoice('https://invoice.etax.nat.gov.tw/')