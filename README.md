<div align=center><img src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Requests_Python_Logo.png" height=500px; width=500px;></div>  
 
--------------------------------------------------

<div align=left></div>  

# web-crawler-by-xpath
運用xpath解析Requests  
關於xpath的詳細用法:https://devhints.io/xpath  
連結所有子節點的text()   descendant::text()  
- 若有SSL憑證問題
在Code中加入
```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### 確認網頁編碼  
```
print(response.encoding)  
print(response.apparent_encoding)  
```

### 清除emoji  
```
import emoji
import re
text = emoji.demojize(text)  
text_demojize = re.sub(':\S+?:', ' ', text)
```
### 清除 u3000...eq 等問題
```
import re
content = re.sub('\s', ' ', content)
```
### 取得tag ID
```
test = <Element Strong at 0x000000>
print(test.tag) # Strong
```

### 轉字體(繁轉簡)
``` 
 from opencc import OpenCC  
 cc = OpenCC('t2s')  
 content = cc.convert(content) 
 ```  

### 批量分割
``` 
import re  
re.split('。|！|？','',text) 
```


### not contains example  
- //div[@class='entry-content']/div[not(contains(@class, 'yarpp-related'))]

### retrying 
- python -m pip install retrying
- from retrying import retry 

- 設置方法的最大延遲時間，默認為100毫秒(是執行這個方法重試的總時間)
@retry(stop_max_attempt_number=5,stop_max_delay=50)  
- 添加每次方法執行之間的等待時間  
@retry(stop_max_attempt_number=5,wait_fixed=2000)  
- 隨機的等待時間  
@retry(stop_max_attempt_number=5,wait_random_min=100,wait_random_max=2000)  
- 每調用一次增加固定時長  
@retry(stop_max_attempt_number=5,wait_incrementing_increment=1000)  

### Fake User-Agent  
```
import fake_useragent import UserAgent  
ua = UserAgent()  
```
**fake UserAgent List**  
-------------------------------
https://developers.whatismybrowser.com/useragents/explore/operating_system_name/?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=breadcrumbs  

### 爬蟲若出現connection reset by peer  
- python -m pip install pyopenssl ndg-httpsclient pyasn1

### 爬蟲若出現HTTP(S)ConnectionPool:Max retries exceed with url
1. 隨手關閉session池
```
import requests
requestss = requests.Session()
requestss.keep_alive = False
```
### 相似詞比對工具  
- 若有兩篇相似之文章需要比對  
```
import difflib
seq = difflib.SequenceMatcher(None, default_msg, new_msg)
ratio = seq.ratio()
```
  
# 改天研究  
https://www.zhihu.com/column/webspider  
https://dotblogs.com.tw/supershowwei/2018/09/03/145254  
https://zhuanlan.zhihu.com/p/32187820  

