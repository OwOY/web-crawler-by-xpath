import requests
from lxml import etree
import prettytable as pt
import os



class parse_baha:

    tb = pt.PrettyTable(['ID','Category','TotalGBP','Title','Interactive','Hot','Last_comment'])

    def __init__(self):
        self.requests = requests.Session()

    def main(self):
        
        bsn = self.choose_board()
        self.get_board_info(bsn)

    def choose_board(self):

        gamer_choose_dict = {
            '1':'場外哈拉版',
            '2':'歡樂惡搞版',
            '3':'Steam版',
            '4':'職場甘苦談',
            '5':'酸甜苦辣版'
        }
        gamer_Link_dict = {
            '場外哈拉版':'60076',
            '歡樂惡搞版':'60084',
            'Steam版' : '60599',
            '職場甘苦談':'60561',
            '酸甜苦辣版':'60091'
        }

        while True:
            choose_gamerindex = str(input('(0)離開(1)場外哈拉版(2)歡樂惡搞版(3)Steam版(4)職場甘苦談(5)酸甜苦辣版\n請選擇你要進入的版面 : '))
            if choose_gamerindex == '0':
                break
            try:
                bsn = gamer_Link_dict[gamer_choose_dict[choose_gamerindex]]
            except:
                print('輸入錯誤請重請輸入')
                os.system('pause')
                continue
        return bsn

    def get_tree(self):
        
        resp = self.requests.get(
                'https://forum.gamer.com.tw/B.php',
                headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'referer': 'https://forum.gamer.com.tw/A.php?bsn=60076',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            },
                params = {
                    'page' : page,
                    'bsn': bsn
                }
            )

        tree = etree.HTML(resp.text)
        return tree

    def get_category_list(self):

        Category_List = []
        Category = T.xpath('.//p[@class="b-list__summary__sort"]//text()')
        [Category_List.append(Category[0])]
        return Category_List
    
    def get_total_gbp(self):
        
        Total_GBP_List = []
        Total_GBP = T.xpath('.//td[@class="b-list__summary"]//span//text()')
        try:
            Total_GBP_List.append(Total_GBP[0])
        except:
            Total_GBP_List.append('0')
        return Total_GBP_List
    def get_title_list(self):

        Title_List = []
        Title = T.xpath('.//div[@class="b-list__tile"]//p//text()')
        [Title_List.append(Title[0])] 
        return Title_List

    def get_urls(self):

        Link_List = []
        Link = T.xpath('.//div[@class="b-list__tile"]//@href')
        [Link_List.append('https://forum.gamer.com.tw/'+Link[0])]
        return Link_List
    def get_react(self):

        Interactive_List = []
        react = T.xpath('.//p[@class="b-list__count__number"]//text()')
        [Interactive_List.append(react[1])]
        return Interactive_List
    
    def get_hot_list(self):

        Hot_List = []
        [Hot_List.append(react[3])]
        return Hot_List
    
    def get_last_comment(self):

        Last_comment_List = []
        Last_comment = T.xpath('.//p[@class="b-list__time__edittime"]//text()')
        [Last_comment_List.append(Last_comment[1])]
        return Last_comment_List

    def get_board_info(self, bsn):

        page  = 1
        while True:
        
            tree = self.get_tree()
            Total = tree.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]')
            
            for T in Total:
                    
            i = 1
            for a,b,c,d,e,f in zip(self.get_category_list(), self.get_total_gbp(),\
                                    self.get_title_list(),self.get_react(),\
                                    self.get_hot_list(),self.get_last_comment()):
                tb.add_row([i,a,b,c,d,e,f])
                i+=1
            print(tb)
            user_choose = int(input('(0)重新選擇版面(1)進入頁面(2)下一頁(3)上一頁(4)取消\n請選擇想要的動作:'))
            
            if user_choose == 0:
                break
            elif user_choose == 1:
                tb1 = pt.PrettyTable(['ID','comment'])
                choose_index = int(input('請選擇想要查看的內文代碼：'))
                p1 = requests.get(Link_List[choose_index-1],headers = h)
                HTML = etree.HTML(p1.text)
                post_time = HTML.xpath('//div[@class="c-post__header__info"]//a//@data-mtime')
                comment = HTML.xpath('//article[@class="c-article FM-P2"]')
                ID = 1
                tb1 = pt.PrettyTable(['ID','comment'])
                for C in comment:
                    D = C.xpath('.//text()')
                    while True:
                        try:
                            D.remove('\n')
                        except:
                            break
                    if D == []:
                        D.append('img')
                    for E in D:
                        if E == D[0]:
                            tb1.add_row([ID, E.strip()])
                        else:
                            tb1.add_row(['',E.strip()])
                    ID += 1
                print(tb1)
                os.system('pause')
            elif user_choose == 2:
                page +=1
            elif user_choose == 3:
                page -=1
                if page ==0:
                    print('已經是第一頁囉~')
                    page = 1
                    os.system('pause')
            elif user_choose == 4:
                continue
            else:
                print('輸入錯誤，請重新輸入')
                os.system('pause')