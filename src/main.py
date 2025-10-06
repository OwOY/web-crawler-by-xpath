from aiohttp import ClientSession
import asyncio
import aiofiles
import base64
import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False, use_gpu=True)

headers = {
    'Host': 'giving.ntu.edu.tw',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
}

process_payload = {
    'item': '148', # 捐款項目
    'frequency': '77', # 捐款頻率
    'currency': 'TWD', # 捐款幣別
    'amount': '500', # 捐款金額
    'total': '500', # 總金額
    'paytype': '139', # 捐款方式
    'name': '龍華', # 捐款人姓名
    'xx_nameEN': 'DDL', # 英文姓名
    'tel': '0915305684', # 電話
    'email': 'abc965@gmail.com', # 電子郵件
    'birthMonth': '11', # 出生月份
    'birthDay': '17', # 出生日期
    ###
    "classifyID":"2", # 校友(若不是則無此參數)
    "graduateYear":"73", # 畢業年份
    "graduateDep":"法律", # 畢業科系
    
    'NTUAAID': None, # 校友會ID
    'subscript': '32', # 是否訂閱電子報
    'TaxType': '132', # 稅務類型
    'receiptName': '龍華', # 收據抬頭
    'identityID': 'F128632017', # 身分證字號
    'send': '1', # 是否寄送收據
    'ThanksMedal': 'N',
    'ReciptType': '136', # 收據類型
    'bePublic': '37', # 是否公開捐款人姓名
    'receiptAddr': '長榮路', # 收據地址
    'address': '長榮路', # 地址(同上)
    'areaCode': '252', # 郵遞區號(前3碼)
    'subAreaCode': '51', # 郵遞區號(後2碼)
    'country': '42', # 國家代碼
    'city': '1', # 城市代碼
    'town': '1', # 市區代碼
    'creatorIP': ''
}


class GivingNTU:
    def __init__(self, session: ClientSession):
        self.session = session

    async def get_captcha(self):
        url = 'https://giving.ntu.edu.tw/backend/CaptchaHandler.ashx'
        async with self.session.get(
            url, 
            params={
                'Mode': 'CreateCaptchaImg',
            },
        ) as response:
            if response.status != 200:
                return '', ''
            data = await response.json(content_type='text/plain; charset=utf-8')
            status = data.get('IsCorrect')
            if not status:
                return '', ''
            captcha_id = data.get('captchaId')
            captcha = data.get('captchBmp')
            captcha_string = captcha.split(',')[1]
            answer = ocr.classification(captcha_string)
            print(answer)
            async with aiofiles.open('captcha.png', 'wb') as f:
                await f.write(
                    base64.b64decode(captcha_string)
                )  # Decode the base64 string
            return captcha_id, answer

    async def post_giving_data(self, payload):
        url = 'https://giving.ntu.edu.tw/backend/CaptchaHandler.ashx'
        async with self.session.post(
            url, 
            data=payload
        ) as response:
            if response.status == 200:
                return await response.json(content_type='text/plain; charset=utf-8')
            
    
async def main():
    payload = {
        'Mode':'SaveGivingDataWithDIYCapcha',
        'CAPTCHAID':'b8a17948-68b3-49ee-8ba9-0438f332ac00',
        'CAPCHAAns':'54784',
        'ProcessString': str(process_payload).replace('None', 'null'),
    }
    
    async with ClientSession(headers=headers) as session:
        giving_ntu = GivingNTU(session)
        captcha_id, answer = await giving_ntu.get_captcha()
        if not captcha_id or not answer:
            print("Failed to get captcha.")
            return
        payload['CAPTCHAID'] = captcha_id
        payload['CAPCHAAns'] = answer
        print(await giving_ntu.post_giving_data(payload))
        

if __name__ == '__main__':
    asyncio.run(main())