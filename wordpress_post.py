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
from random import randint
import datetime


mongoclient = pymongo.MongoClient('192.168.1.141')
collection = mongoclient['mouzhan_org']['国产原创']

wp = Client('https://taflower.cn/xmlrpc.php','taflowerA','ib43CfrHPU6Fzn')
post = WordPressPost()

def get_post_ok_list():

    post_ok_title_list = []
    for data in mongoclient['taflower_post']['post_OK'].find():
        post_ok_title_list.append(data['title'])

    return post_ok_title_list

def get_post_fail_list():

    post_fail_title_list = []
    for data in mongoclient['taflower_post']['post_fail'].find():
        post_fail_title_list.append(data['title'])

    return post_fail_title_list

def set_cover(cover_url):

    img = requests.get(cover_url).content
    img_data = {'name':'test.jpg', 'type':'image/jpeg'}
    img_data['bits'] = xmlrpc_client.Binary(img)

    return img_data

def set_contents(contents, imgs):
    
    _contents = ''
    random_post = randint(0, len(contents)-1)
    for content in contents:
        if content == contents[random_post]:
            _contents += '<p style="font-size:62px !important"><a href="http://bit.ly/3pQ4328" class="rank-math-link"><span class="has-inline-color has-vivid-red-color">点我观看</span></a></p>'
        if content in imgs:
            _contents += '<figure class="wp-block-image size-large"><img src= "'+ content+'" alt=""/></figure>'
            _contents += '<br>'
        else:
            _contents += content
            _contents += '<br>'
    _contents += '更多影片，下载，播放 欢迎<p style="font-size:62px !important"><a href="http://bit.ly/3pQ4328" class="rank-math-link"><span class="has-inline-color has-vivid-red-color">点我</span></a></p>看更多'

    return _contents


for data in collection.find():

    if data['title'] not in get_post_ok_list():

        img_data = set_cover(data['cover'])
        contents = set_contents(data['content'], data['imgs'])

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        try:
            response = wp.call(media.UploadFile(img_data))
            post.thumbnail = response['id']
            post.post_status = "publish"
            title = data['title']
            post.title = str(title)
            post.content = contents
            post.terms_names = {'category': ['探花',]}
            post_id = wp.call(NewPost(post))
            mongoclient['taflower_post']['post_OK'].insert_one({'title':data['title'], 'time':f"{datetime.date.today()}_{current_time}", 'category':data['category']})
            print(f"{data['title']}  post   ok")
        except:
            if data['title'] not in get_post_fail_list():
                mongoclient['taflower_post']['post_fail'].insert_one({'title':data['title'], 'time':f"{datetime.date.today()}_{current_time}", 'category':data['category']})
            print(f"{data['title']}   post   fail")