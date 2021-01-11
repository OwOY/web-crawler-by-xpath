# web-crawler-by-xpath
運用xpath解析Requests  
關於xpath的詳細用法:https://devhints.io/xpath  
連結所有子節點的text()   descendant::text()  

## 常用指令  
### 清除emoji  
```
text = emoji.demojize(sen1)  
text = re.sub(':\S+?:', ' ', text)
```
### 如果String長['test']  
- 可以使用eval(string)轉換成List  

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

### 多進程的運用  
``` from multiprocessing import Process  
    def run5_post(x):  
    run(x)
    if __name__ == '__main__':      
        t1 = Process(target=run5_post, args=(1,))  
        t2 = Process(target=run5_post, args=(2,))  
        t1.start()  
        t2.start()  
```
### not contains example  
- //div[@class='entry-content'][not(contains(div/@class, 'yarpp-related'))]

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
  

  
# 改天研究  
https://www.zhihu.com/column/webspider  
https://dotblogs.com.tw/supershowwei/2018/09/03/145254  
https://zhuanlan.zhihu.com/p/32187820  
