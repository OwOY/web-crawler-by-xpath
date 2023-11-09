import requests
from lxml import etree
import prettytable as pt
import os

class News:
    
    def __init__(self):

        self.requests = requests.Session()
        self.main()


    def main(self):
        
        self.get_news_category()


    def get_tree(self, url):
        
        response = self.requests.get(url, headers = {
            'Host': 'cn.nytimes.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
        }).text
        
        html = etree.HTML(response)
        return html
    

    def get_news_category(self):
        
        tb = pt.PrettyTable(['ID', 'Category'])
        html = self.get_tree('https://cn.nytimes.com/lens/')
        categorys = html.xpath('//div[@id="nav"]/ul/li//a/text()')[1:-1]
        category_links = html.xpath('//div[@id="nav"]/ul/li//a/@href')[1:-1]
        category_links = [f'https://cn.nytimes.com{category_link}' for category_link in category_links]
        i = 1
        for category in categorys:
            # print(i, f'https://cn.nytimes.com{category_link}')
            tb.add_row([i, f'{category}'])
            i += 1
        print(tb)
        self.choose_category(category_links)


    def choose_category(self, urls):
        
        while True:
            user_choose = int(input('請選擇你要的動作(0)離開(1)進入面板 : '))
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                try:
                    choose_board = int(input('請選擇要進入的面板 : '))
                    self.get_article_list(urls[choose_board - 1], 1)
                except:
                    print('請重新輸入')
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
            else:
                print('請重新輸入')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
    
    
    def get_article_list(self, category_url, page):

        tb = pt.PrettyTable(['ID','Title'])
        link = f'{category_url}{page}/'
        html = self.get_tree(link)
        articles = html.xpath('//div[@id="sectionLeadPackage"]//h3/a/@title|//div[@class="sectionAutoList columnAplusB "]//h3/a/@title')
        article_links = html.xpath('//div[@id="sectionLeadPackage"]//h3/a/@href|//div[@class="sectionAutoList columnAplusB "]//h3/a/@href')
        article_links = [f'https://cn.nytimes.com{article_link}' for article_link in article_links]
        i = 1
        for article in articles:
            tb.add_row([i, article])
            i += 1
        self.choose_article(category_url, page, article_links, tb)
    

    def choose_article(self, category_url, page, urls, tb):
        
        while True:
            print(tb)
            user_choose = int(input('請選擇你要的動作(0)離開(1)進入文章(2)上一頁(3)下一頁(4)重新選擇分類 : '))
            if user_choose == 0:
                os._exit(0)
            elif user_choose == 1:
                choose_article = int(input('請選擇文章 : '))
                try:
                    self.get_content(urls[choose_article - 1])
                except:            
                    print('請重新輸入')
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
            elif user_choose == 2:
                if page == 1:
                    print('這是第1頁囉')
                    # os.system('pause')   #windows選擇使用
                    os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用
                else:
                    page -= 1
                    self.get_article_list(category_url, page)
            elif user_choose == 3:
                page += 1
                self.get_article_list(category_url, page)
            elif user_choose == 4:
                self.get_news_category()
            else:
                print('請重新輸入')
                # os.system('pause')   #windows選擇使用
                os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用


    def get_content(self, url):

        html = self.get_tree(url)
        contents = html.xpath('//div[@class="article-paragraph"]//text()|//div[@class="article-paragraph"]//img/@src')
        for content in contents:
            print(content)
        # os.system('pause')   #windows選擇使用
        os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用

if __name__ == '__main__':

    News()