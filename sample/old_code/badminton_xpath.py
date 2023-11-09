import requests
from lxml import etree
import prettytable as pt
import os


class badmintontw:


    def __init__(self, date):
        self.tb = pt.PrettyTable(['ID','Team','Country','Time','Location','Lv','Fee','Court','Ball'])
        self.requests = requests.Session()
        self.date = date
        self.main()


    def main(self):
        tb = self.get_team_info()
        self.choose_team(tb)


    def get_html(self, url):

        resp = self.requests.get(url,headers = 
                {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            },params = {
                'date':self.date
            }).text
        html = etree.HTML(resp)
        return html


    def get_team(self, html):

        Team = html.xpath('//td[@class="name"]')
        Team = [T.xpath('.//text()') for T in Team]
        Team =  [T[0] if T != [] else '??' for T in Team]
        return Team


    def get_country(self, html):

        Country = html.xpath('//td[2]')
        Country = [C.xpath('.//text()') for C in Country]
        Country = [C[0] if C != [] else '??' for C in Country]
        return Country


    def get_time(self, html):

        Time = html.xpath('//td[3]')
        Time = [T.xpath('.//text()') for T in Time]
        Time = [T[0] if T != [] else '??' for T in Time]
        return Time


    def get_location(self, html):

        Location = html.xpath('//td[4]')
        Location = [L.xpath('.//text()') for L in Location]
        Location = [L[0] if L != [] else '??' for L in Location]
        return Location


    def get_lv(self, html):

        Lv = html.xpath('//td[5]')
        Lv = [L.xpath('.//text()') for L in Lv]
        Lv = [L[0] if L != [] else '??' for L in Lv]
        return Lv


    def get_fee(self, html):

        Fee = html.xpath('//td[6]')
        Fee = [F.xpath('.//text()') for F in Fee]
        Fee = [F[0] if F != [] else '??' for F in Fee]
        return Fee


    def get_court(self, html):

        Court = html.xpath('//td[7]')
        Court = [C.xpath('.//text()') for C in Court]
        Court = [C[0] if C != [] else '??' for C in Court]
        return Court


    def get_ball(self, html):
        
        Ball = html.xpath('//td[8]')
        Ball = [B.xpath('.//text()') for B in Ball]
        Ball = [B[0] if B != [] else '??' for B in Ball]
        return Ball


    def get_team_detail_link(self, html):

        Get_Link = html.xpath('//td[4]')
        Get_Link = ['https://www.badmintontw.com/'+GL.xpath('.//@href')[0] for GL in Get_Link]
        return Get_Link


    def get_team_info(self):

        html = self.get_html('https://www.badmintontw.com/taipei.php')
        # -------------------------------------------------------------------------------
        Team = self.get_team(html)
        Country = self.get_country(html)
        Time = self.get_time(html)
        Location = self.get_location(html)
        Lv = self.get_lv(html)
        Fee = self.get_fee(html)
        Court = self.get_court(html)
        Ball = self.get_ball(html)
        id = 1
        for a,b,c,d,e,f,g,h in zip(Team,Country,Time,Location,Lv,Fee,Court,Ball):
            self.tb.add_row([id,a,b,c,d,e,f,g,h])
            id += 1

        return self.tb


    def choose_team(self, tb):
        
        html = self.get_html('https://www.badmintontw.com/taipei.php')
        # -------------------------------------------------------------------------------
        team = self.get_team(html)
        # -------------------------------------------------------------------------------
        get_Link = self.get_team_detail_link(html)
        # -------------------------------------------------------------------------------
        while True:
            print(tb)
            select = int(input('請選擇想要的球隊ID或選擇 0 離開 : '))
            if select == 0:
                break
            link = get_Link[select-1]
            self.get_team_detail(link, team, select)


    def get_need_ppl(self, html):

        need_ppl = html.xpath('//ul[@class="no-padding-left"]//li[2]//text()')
        need_ppl = [NP.strip() for NP in need_ppl]
        need_ppl = ''.join(need_ppl)
        return need_ppl
    

    def get_detail_location(self, html):

        detail_location = html.xpath('//ul[@class="no-padding-left"]//li[5]//text()')
        detail_location = [DL.strip().strip('()').replace('地圖','') for DL in detail_location]
        detail_location = ''.join(detail_location)
        return detail_location


    def get_tel(self, html):

        tel = html.xpath('//li[label[@for="contact_phone1"]]//text()')
        tel = [T.strip().strip('(撥打)簡訊') for T in tel]
        tel = ''.join(tel)
        return tel


    def get_contact_name(self, html):

        contact_name = html.xpath('//li[label[@for="contact_person1"]]//text()')
        contact_name = [t.strip() for t in contact_name]
        contact_name = ''.join(contact_name)
        return contact_name


    def get_contact_line(self, html):

        line = html.xpath('//li[label[contains(text(),"Line")]]//text()')
        line = [T.replace('傳Line訊息','').strip('()') for T in line]
        line = ''.join(line)
        return line


    def get_team_detail(self, link, team, select):

        html = self.get_html(link)
        # -------------------------------------------------------------------------------
        need_ppl = self.get_need_ppl(html)
        detail_location = self.get_detail_location(html)
        tel = self.get_tel(html)
        contact_name = self.get_contact_name(html)
        line = self.get_contact_line(html)
        # -------------------------------------------------------------------------------
        print(team[select-1], need_ppl, detail_location, contact_name, tel, line)
        # -------------------------------------------------------------------------------
        os.system('read -n 1 -p "Press any key to continue..."')


if __name__ == '__main__':
    date = input('請輸入今天日期(請按照格式:月/日) : ')
    badmintontw(date)
