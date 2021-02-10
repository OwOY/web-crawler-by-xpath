import requests
import prettytable as pt
from lxml import etree
import os
import json

class Dcard_horoscope:

    def __init__(self):

        self.requests = requests.Session()
        self.main()
    
    def main(self):

        self.get_article_list('https://www.dcard.tw/service/api/v2/forums/horoscopes/posts?popular=true&limit=30')


    def get_tree(self, url):

        h = {
                    'Host': 'www.dcard.tw',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Cookie': '__cfduid=d043f4381bec87c48df7b199ba78c36921592574408; dcsrd=wzYupjK9-4rPWoZK-kgcIZTI; dcsrd.sig=aMutTs7K3XR1RQj7l7jZ4zNC6Ug; __asc=698b752b172ccd66e60423e1f66; __auc=698b752b172ccd66e60423e1f66; _ga=GA1.1.1003447311.1592574505; _ga_C3J49QFLW7=GS1.1.1592574504.1.1.1592574594.0',
                    'Upgrade-Insecure-Requests': '1'
        }

        resp = self.requests.get(
            url,headers = h,
        ).text
        tree = etree.HTML(resp)
        return tree

        
    def get_json(self, url):

        h = {
                    'Host': 'www.dcard.tw',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Cookie': '__cfduid=d043f4381bec87c48df7b199ba78c36921592574408; dcsrd=wzYupjK9-4rPWoZK-kgcIZTI; dcsrd.sig=aMutTs7K3XR1RQj7l7jZ4zNC6Ug; __asc=698b752b172ccd66e60423e1f66; __auc=698b752b172ccd66e60423e1f66; _ga=GA1.1.1003447311.1592574505; _ga_C3J49QFLW7=GS1.1.1592574504.1.1.1592574594.0',
                    'Upgrade-Insecure-Requests': '1'
        }

        resp = self.requests.get(
            url,headers = h,
        ).json()
        return resp


    def get_article_list(self, url):
        
        tb = pt.PrettyTable(['ID','Like','Response','Title'])
        resp = self.get_json(url)
        i = 1
        link_list = []
        for data in resp:
            article_ID = data['id']
            tb.add_row([i, data['likeCount'], data['commentCount'], data['title'], ])
            link_list.append(f'https://www.dcard.tw/f/horoscopes/p/{article_ID}')
            i += 1
        print(tb)
        self.choose_article(tb, link_list)


    def choose_article(self, tb, link_list):

        urlID = link_list[-1].split('/')[-1]
        choose = int(input('(0)離開(1)進入內文(2)下一頁(3)上一頁\t請選擇您的動作 : '))
        if choose == 0:
            os._exit(0)
        elif choose == 1:
            article_ID = int(input('請選擇要進入的頁面 : '))
            self.get_article_content(link_list[article_ID - 1])
            self.get_article_list('https://www.dcard.tw/service/api/v2/forums/horoscopes/posts?popular=true&limit=30')
        elif choose == 2:
            self.get_article_list(f'https://www.dcard.tw/service/api/v2/forums/horoscopes/posts?popular=true&limit=30&before={urlID}')
        elif choose == 3:
            self.get_article_list(f'https://www.dcard.tw/service/api/v2/forums/horoscopes/posts?popular=true&limit=30&before={urlID}')
        else:
            print('輸入錯誤，請重新輸入')
            # os.system('pause')   #windows選擇使用
            os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用


    def get_article_content(self, url):

        tree = self.get_tree(url)
        articles = tree.xpath('//div[@class="sc-1eorkjw-5 fhXuqT"]//text()|//div[@class="sc-1eorkjw-5 fhXuqT"]//img/@src')
        comment_list = tree.xpath('//div[@class="sc-1bx44oc-5 fmKQGq"]//div[@class="pj3ky0-3 fIApHl"]')
        comment_list = [''.join(comment.xpath('.//text()')) for comment in comment_list]
        commentlike_list = tree.xpath('//div[@class="jt7qse-0 dtTasy"]/label/text()')
        i = 0
        for article in articles:
            print(article)
        while i < len(comment_list):
            print(f'Like: {commentlike_list[i]}\n{comment_list[i]}')
            print('====================================')
            i += 1
        # os.system('pause')   #windows選擇使用
        os.system('read -n 1 -p "Press any key to continue..."')    #Linux選擇使用

if __name__ == '__main__':

    Dcard_horoscope()
    # Dcard_horoscope().get_article_content('https://www.dcard.tw/f/horoscopes/p/235260084')