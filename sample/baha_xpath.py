import requests
from lxml import etree
import prettytable as pt
import os


class baha_gossiping:

    def __init__(self):

        self.requests = requests.Session()
        self.main()


    def main(self):
    
        self.get_board_list(1)


    def get_tree(self, url):
        
        resp = self.requests.get(url, headers = {
            'Host': 'forum.gamer.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://forum.gamer.com.tw/',
        }).text

        html = etree.HTML(resp)
        return html


    def get_json(self, url, page):
        
        resp = self.requests.get(url, headers = {
            'Host': 'forum.gamer.com.tw',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://forum.gamer.com.tw/',
        },params = {
            'c':'21',
            'page':page
        }).json()

        return resp

    
    def get_board_list(self, page):
        
        id = 1
        board = pt.PrettyTable(['ID', 'rank', 'board_name'])
        resp = self.get_json('https://forum.gamer.com.tw/ajax/rank.php', page)
        bsns = []
        for data in resp:
            board.add_row([id, data['ranking'], data['title']])
            bsns.append(data['bsn'])
            id += 1
        print(board)
        return self.choose_board(bsns, page)


    def choose_board(self, bsns, page):

        while True:
            try:
                user_choose = int(input('請選擇你的動作 (0)退出(1)進入版面(2)上一頁(3)下一頁 : '))
            except:
                print('請重新輸入')
                continue
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                try:
                    choose_board = int(input('請選擇進入版面 :'))
                except:
                    print('請重新輸入')
                    continue
                self.get_article_list(bsns[choose_board-1], 1)
            elif user_choose == 2:
                if page == 1:
                    print('已經是第1頁囉')
                    page = 1
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                else:
                    page -= 1
                self.get_board_list(page)
            elif user_choose == 3:
                page += 1
                self.get_board_list(page)
            else:
                print('請重新輸入')


    def get_article_list(self, bsn, page):
        
        id = 1
        tb = pt.PrettyTable(['ID', 'category', 'hot', 'title' , 'react', 'view'])
        html = self.get_tree(f'https://forum.gamer.com.tw/B.php?bsn={bsn}&page={page}')
        category_list = html.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]/td[1]//p/a/text()')
        hot_list = html.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]/td[1]')
        hot_list = [hot.xpath('.//span/text()')[0] if hot.xpath('.//span/text()') != [] else '0' for hot in hot_list]
        title_list = html.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]/td[2]//div[@class="b-list__tile"]/p/text()')
        article_urls = html.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]/td[2]/a/@href')
        react_list = html.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]/td[3]/p[1]/span[1]/text()')
        view_list = html.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]/td[3]/p[1]/span[2]/text()')
        for a, b, c, d, e in zip(category_list, hot_list, title_list, react_list, view_list):
            tb.add_row([id, a, b, c, d, e])
            id += 1
        print(tb)
        return self.choose_article(article_urls, bsn, page)


    def choose_article(self, article_urls, bsn, page):
        
        while True:
            try:
                user_choose = int(input('請選擇你的動作 (0)離開(1)進入文章(2)上一頁(3)下一頁(4)重新選版 : '))
            except:
                print('請重新輸入')
                continue
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                try:
                    choose_article = int(input('請選擇文章 : '))
                except:
                    print('請重新輸入')
                    continue
                self.get_article_content(f'https://forum.gamer.com.tw/{article_urls[choose_article-1]}', bsn)
            elif user_choose == 2:
                if page == 1:
                    print('已經是第1頁囉')
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                else:
                    page -= 1
                    self.get_article_list(bsn, page)
            elif user_choose == 3:
                page += 1
                self.get_article_list(bsn, page)
            elif user_choose == 4:
                self.get_board_list(1)
            else:
                print('輸入錯誤')
    

    def get_article_content(self, url, bsn):

        page = 1
        html = self.get_tree(url)
        last_page = html.xpath('//p[@class="BH-pagebtnA"]/a[last()]/text()')

        while True:
            html = self.get_tree(f'{url}&page={page}')
            tb = pt.PrettyTable(['User', 'Comment', 'Good', 'Bad'])
            username_list = html.xpath('//a[@class="username"]/text()')
            comment_list = html.xpath('//div[@class="c-article__content"]')
            comment_list = [''.join(comment.xpath('.//text()')) for comment in comment_list]
            gp_list = html.xpath('//div[@class="gp"]/a/text()')
            bp_list = html.xpath('//div[@class="bp"]/a/text()')
            for a, b, c, d in zip(username_list, comment_list, gp_list, bp_list):
                tb.add_row([a, b, c, d])
            print(tb)

            user_choose = int(input('請選擇動作(0)退出(1)上一頁(2)下一頁(3)重新選擇文章 : '))
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                if page == 1:
                    print('已經是第1頁囉')
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                else:
                    page -= 1
            elif user_choose == 2:
                if page == int(last_page[0]):
                    print('已經最後一頁囉')    
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                else:
                    page += 1
            elif user_choose == 3:
                self.get_article_list(bsn, 1)
            else:
                print('請重新輸入')

if __name__ == '__main__':

    baha_gossiping()
    # baha_gossiping().get_article_list(23835)