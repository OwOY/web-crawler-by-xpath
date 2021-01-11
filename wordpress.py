from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
import pymongo
from time import sleep
import codecs
import os
import requests
from lxml import etree

mongoclient = pymongo.MongoClient('192.168.1.141')
collection = mongoclient['lulupig_cn']['大神探花']
wp = Client(url,account,password)
post = WordPressPost()

_contents = ''

class mouzhan:

    def __init__(self, url):
        self.url = url

    def get_xpath(self):

        resp = requests.get(self.url,headers = {
                'Host': 'mouzhan.org',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive'
        }).text

        html = etree.HTML(resp)
        return html    

    def get_title(self):
        
        html = self.get_xpath()
        title = html.xpath('//h1[@class="entry-title"]/text()')
        return title

    def get_contents(self):

        html = self.get_xpath()
        imgs = html.xpath('//div[@id="deawfgregs"]//img/@src')
        contents = html.xpath('//div[@id="deawfgregs"]//img/@src|//div[@id="deawfgregs"]')
        _contents = ''
        for content in contents:
            if content in imgs:
                _contents += '<figure class="wp-block-image size-large"><img src= "'+ content+'" alt=""/></figure>'
                _contents += '<br>'
            else:
                if '種子' not in content:
                    _contents += content
                    _contents += '<br>'
        _contents += '更多影片，下载，播放 欢迎到:<p style="font-size:62px !important"><a href="https://google.com" class="rank-math-link"><span class="has-inline-color has-vivid-red-color">Ares</span></a></p> 看更多'
        return _contents
        
    def download_cover(self):
        
        html = self.get_xpath()
        imgs = html.xpath('//div[@id="deawfgregs"]/p//img/@src')
        img = requests.get(imgs[0]).content
        # with codecs.open('E:/1.jpg','wb')as f:
        #     f.write(img)        
        return img

