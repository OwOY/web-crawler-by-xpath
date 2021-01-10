import requests
from lxml import etree
import prettytable as pt
import os

tb = pt.PrettyTable(['ID','Name','Class','Title'])

requests = requests.Session()

h = {
        'Host': 'www.ptt.cc',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

p = requests.get(
    'https://www.ptt.cc/bbs/index.html',
    headers = h
)

HTML = etree.HTML(p.text)
#------------------------------------------------------------------------
board_name  = HTML.xpath('//div[@class="board-name"]/text()')
#------------------------------------------------------------------------
board_class = HTML.xpath('//div[@class="board-class"]/text()')
# ------------------------------------------------------------------------
board_title = HTML.xpath('//div[@class="board-title"]/text()')
# ------------------------------------------------------------------------
board_link  = HTML.xpath('//a[@class="board"]/@href')
board_link  = ['https://www.ptt.cc/'+bl for bl in board_link]
# ------------------------------------------------------------------------
i = 1
for a,b,c in zip(board_name, board_class, board_title):
    tb.add_row([i,a,b,c])
    i += 1
while True:
    print(tb)

    board_select = int(input('請選擇要進入的版面或是輸入(0)離開 : '))
    if board_select == 0:
        break
    p1 = requests.get(board_link[board_select-1],headers = h,cookies={'over18': '1'})

    while True:
        tb1 = pt.PrettyTable(['ID','Hot','Title','Date'])
        HTML1 = etree.HTML(p1.text)
        # ------------------------------------------------------------------------
        Title = HTML1.xpath('//div[@class="title"]')
        Title = [''.join(T.xpath('.//text()')).strip() for T in Title]
        # ------------------------------------------------------------------------
        Date = HTML1.xpath('//div[@class="date"]')
        Date = [''.join(D.xpath('.//text()')).strip() for D in Date]
        # ------------------------------------------------------------------------
        Title_Link = HTML1.xpath('//div[@class="title"]')
        Title_Link = ['https://www.ptt.cc/'+''.join(TL.xpath('.//@href')) for TL in Title_Link]
        # ------------------------------------------------------------------------
        Hot = HTML1.xpath('//div[@class="r-ent"]')
        Hot = [H.xpath('.//span//text()') for H in Hot]
        Hot = [H[0] if len(H) >= 1 else '0' for H in Hot]
        # ------------------------------------------------------------------------
        j = 1
        for a,b,c in zip(Hot,Title, Date):
            tb1.add_row([j,a,b,c])
            j+=1
        print(tb1)
        action = int(input('請選擇(0)重新選擇版面(1)進入頁面(2)下一頁(3)上一頁 : '))
        if action == 0:
            break
        elif action == 1:
            title_select = int(input('請選擇要進入的頁面 : '))
            p2 = requests.get(Title_Link[title_select-1], headers = h, cookies = {'over18':'1'})
            HTML2 = etree.HTML(p2.text)
            text = HTML2.xpath('//div[@id="main-content"]//text()')
            text = ''.join(text)
            os.system('cls')
            print('\n'+text)
            os.system('pause')
            os.system('cls')
        elif action == 2:
            next_page = HTML1.xpath('//a[@class="btn wide"][text()="下頁 ›"]//@href')
            try:
                next_page = 'https://www.ptt.cc/'+next_page[0]
                p1 = requests.get(next_page, headers = h, cookies = {'over18':'1'})
            except:
                print('這是最後一頁囉')
                os.system('pause')
                os.system('cls')
        elif action == 3:
            last_page = HTML1.xpath('//a[@class="btn wide"][text()="‹ 上頁"]//@href')
            try:
                last_page = 'https://www.ptt.cc/'+last_page[0]
                p1 = requests.get(last_page, headers = h, cookies = {'over18':'1'})
            except:
                print('這是第一頁囉')
                os.system('pause')
                os.system('cls')
        