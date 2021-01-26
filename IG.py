import requests
from lxml import etree
import json
import os
import codecs

class IG_image:
    
    def __init__(self, account):

        self.requests = requests.Session()
        self.account = account
        self.main()


    def main(self):

        account_id = self.get_account_id()
        after = ''
        while True:
            resp_json = self.get_json(account_id, after)
            after = self.get_images_urls(resp_json)


    def get_account_id(self):
        
        resp = self.requests.get(
            'https://imginn.com/pyoapple/',
            headers= {
                'Host': 'imginn.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
        ).text
        html = etree.HTML(resp)
        get_account_id = html.xpath('//button[@class="load-more"]/@data-id')
        return get_account_id[0]


    def get_json(self, account_id, after):

        variables = {"id":account_id,"first":12,"after":after}
        variables = str(variables).replace("'",'"').replace(' ','')

        resp = self.requests.get(f'https://www.instagram.com/graphql/query/',
                            headers = {
                                'Host': 'www.instagram.com',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                                'Accept': '*/*',
                                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate',
                                'Origin': 'https://imginn.com',
                                'DNT': '1',
                                'Connection': 'keep-alive'
                            },params = {
                                'query_hash':'56a7068fea504063273cc2120ffd54f3',
                                'variables': variables
                            }).text
    
        resp_json = json.loads(resp)
    
        return resp_json
    

    def get_images_urls(self, resp_json):

        for data in resp_json['data']['user']['edge_owner_to_timeline_media']['edges']:
            self.download_image(data['node']['display_url'])
        end_cursor = resp_json['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        return end_cursor


    def download_image(self, image_url):
        
        resp = self.requests.get(image_url, headers = {
            'Host': 'scontent-sin6-1.cdninstagram.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }).content

        number = 0

        while f'{number}.jpg' in os.listdir(r'E:/python/VS/IGimg'):
            number += 1

        with codecs.open(f'E:/python/VS/IGimg/{str(number)}.jpg','wb')as f:
            f.write(resp)
            print(f'{number}.jpg  download OK')
    

if __name__ == '__main__':
    
    IG_image('pyoapple')
