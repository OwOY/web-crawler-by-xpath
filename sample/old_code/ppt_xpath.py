import requests
from lxml import etree
import prettytable as pt
import os

class Ptt:

    def __init__(self):

        self.requests = requests.Session()
        self.main()
    
    def main(self):
        
        self.get_board_list()
    

    def get_tree(self, url):
        
        resp = self.requests.get(url, cookies={'over18': '1'}, headers = {
                'Host': 'www.ptt.cc',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }).text
        html = etree.HTML(resp)
        return html


    def get_board_list(self):
        
        tb = pt.PrettyTable(['ID','Name','Class','Title'])
        html = self.get_tree('https://www.ptt.cc/bbs/index.html')
        #------------------------------------------------------------------------
        board_name  = html.xpath('//div[@class="board-name"]/text()')
        #------------------------------------------------------------------------
        board_class = html.xpath('//div[@class="board-class"]/text()')
        # ------------------------------------------------------------------------
        board_title = html.xpath('//div[@class="board-title"]/text()')
        # ------------------------------------------------------------------------
        board_link  = html.xpath('//a[@class="board"]/@href')
        board_link  = ['https://www.ptt.cc/'+bl for bl in board_link]
        # ------------------------------------------------------------------------
        i = 1
        for a,b,c in zip(board_name, board_class, board_title):
            tb.add_row([i,a,b,c])
            i += 1
        while True:
            print(tb)
            self.choose_board(board_link)


    def choose_board(self, board_link):
    
        try:
            board_select = int(input('請選擇要進入的版面或是輸入(0)離開 : '))
        except Exception as Ptt:
            print(f'{Ptt}請重新輸入')
            # os.system('pause')   #windows選擇使用
            os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
        if board_select == 0:
            os._exit(0)
        else:
            try:
                self.get_article_list(board_link[board_select-1])
            except Exception as Ptt:
                print(f'{Ptt}請重新輸入')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用


    def get_article_list(self, url):

        tb = pt.PrettyTable(['ID','Hot','Title','Date'])
        html = self.get_tree(url)
        # ------------------------------------------------------------------------
        title = html.xpath('//div[@class="title"]')
        title = [''.join(T.xpath('.//text()')).strip() for T in title]
        # ------------------------------------------------------------------------
        date = html.xpath('//div[@class="date"]')
        date = [''.join(D.xpath('.//text()')).strip() for D in date]
        # ------------------------------------------------------------------------
        title_Link = html.xpath('//div[@class="title"]')
        title_Link = ['https://www.ptt.cc/'+''.join(TL.xpath('.//@href')) for TL in title_Link]
        # ------------------------------------------------------------------------
        hot = html.xpath('//div[@class="r-ent"]')
        hot = [H.xpath('.//span//text()') for H in hot]
        hot = [H[0] if len(H) >= 1 else '0' for H in hot]
        # ------------------------------------------------------------------------
        j = 1
        for a,b,c in zip(hot,title, date):
            tb.add_row([j,a,b,c])
            j+=1
        while True:
            print(tb)
            self.choose_article(url, title_Link)


    def choose_article(self, url, title_Link):

        html = self.get_tree(url)
        try:
            action = int(input('請選擇(0)離開(1)進入頁面(2)下一頁(3)上一頁(4)重新選擇版面 : '))
        except Exception as Ptt:
            print(f'{Ptt}請重新輸入')
            # os.system('pause')   #windows選擇使用
            os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
        if action == 0:
            os._exit(0)
        elif action == 1:
            try:
                title_select = int(input('請選擇要進入的頁面 : '))
                self.get_article_content(title_Link[title_select-1])
            except Exception as Ptt:
                print(f'{Ptt}請重新輸入')
            # os.system('pause')   #windows選擇使用
            os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
        elif action == 2:
            next_page = html.xpath('//a[@class="btn wide"][text()="下頁 ›"]//@href')
            try:
                next_page = 'https://www.ptt.cc/'+next_page[0]
                self.get_article_list(next_page)
            except:
                print('這是最後一頁囉')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
        elif action == 3:
            last_page = html.xpath('//a[@class="btn wide"][text()="‹ 上頁"]//@href')
            try:
                last_page = 'https://www.ptt.cc/'+last_page[0]
                self.get_article_list(last_page)
            except:
                print('這是第一頁囉')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
        elif action == 4:
            self.get_board_list()


    def get_article_content(self, url):

        html = self.get_tree(url)
        text = html.xpath('//div[@id="main-content"]//text()')
        text = ''.join(text)
        print('\n'+text)


if __name__ == '__main__':
    Ptt()