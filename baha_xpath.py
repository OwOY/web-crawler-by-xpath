import requests
from lxml import etree
import prettytable as pt
import os
requests = requests.Session()

page  = 1

h = {
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
        }

while True:
    tb = pt.PrettyTable(['ID','Category','TotalGBP','Title','Interactive','Hot','Last_comment'])
    p = requests.get(
        'https://forum.gamer.com.tw/B.php?page={0}&bsn=60076'.format(page),
        headers = h
    )

    Total = etree.HTML(p.text)

    Total = Total.xpath('//tr[@class="b-list__row b-list-item b-imglist-item"]')
    Category_List = []
    Total_GBP_List = []
    Title_List = []
    Interactive_List = []
    Hot_List = []
    Last_comment_List = []
    Link_List = []
    for T in Total:
        Category = T.xpath('.//p[@class="b-list__summary__sort"]//text()')
        [Category_List.append(Category[0])]
        
        Total_GBP = T.xpath('.//td[@class="b-list__summary"]//span//text()')
        try:
            Total_GBP_List.append(Total_GBP[0])
        except:
            Total_GBP_List.append('0')
            
        Title = T.xpath('.//div[@class="b-list__tile"]//p//text()')
        [Title_List.append(Title[0])] 
        
        Link = T.xpath('.//div[@class="b-list__tile"]//@href')
        [Link_List.append('https://forum.gamer.com.tw/'+Link[0])]
        react = T.xpath('.//p[@class="b-list__count__number"]//text()')
        [Interactive_List.append(react[1])]
        [Hot_List.append(react[3])]
        
        Last_comment = T.xpath('.//p[@class="b-list__time__edittime"]//text()')
        [Last_comment_List.append(Last_comment[1])]
    i = 1
    for a,b,c,d,e,f in zip(Category_List,Total_GBP_List,Title_List,Interactive_List,Hot_List,Last_comment_List):
        tb.add_row([i,a,b,c,d,e,f])
        i+=1
    print(tb)
    user_choose = int(input('(0)離開(1)進入頁面(2)下一頁(3)上一頁(4)取消\n請選擇想要的動作:'))
    
    if user_choose == 0:
        break
    elif user_choose == 1:
        tb1 = pt.PrettyTable(['ID','comment'])
        choose_index = int(input('請選擇想要查看的內文代碼：'))
        p1 = requests.get(Link_List[choose_index-1],headers = h)
        HTML = etree.HTML(p1.text)
        post_time = HTML.xpath('//div[@class="c-post__header__info"]//a//@data-mtime')
        comment = HTML.xpath('//article[@class="c-article FM-P2"]//text()')
        while True:
            try:
                comment.remove('\n')
            except:
                break
        for C in comment:
            print(C)
        j = 1
        # for C in comment:
            # tb1.add_row([j,C.strip()])
            # j+=1
        # print(tb1)
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