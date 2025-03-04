import csv
import os
import random

from scrapy import Request
from scrapy.spiders import Spider

from scrapy import Request
from scrapy.spiders import Spider

class MerchantSpider(Spider):
    name = 'ebo_merchant'
    custom_settings = {
        'DOWNLOAD_DELAY': random.randint(1, 2),  # 设置请求间隔为1秒
    }
    # 设置用户代理（浏览器类型）
    ebo_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Host": "cees.ebopark.com",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://cees.ebopark.com/visitorappointment",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": {'acw_tc': '0b3c7d8216948528815371491ed58978dc5cb314b777e94180eb2180ec5fc6', 'ebopark_session': 'eyJpdiI6ImdFUXFBazlSbUUwbkpvb1FzRHlvUnc9PSIsInZhbHVlIjoiZ3NKYzBpWUVuemdqcE9PdHYyU1A3VE4rN05uMER5MnhmSEFhTSt0XC9hdGQ1ZlFxMGdNc1BhOElHV2ZHYXI0XC9TIiwibWFjIjoiMzM2NDJiMmY2YjcxYjRlMWMzN2JmNWM2ZTgyMjJiZTIwODFhZjA3ZDg5MDUwNTk4YmU4ZjUyYjZkYjZmYTg5YyJ9'}
    }
    ebo_cookie = {'acw_tc': '0b3c7d8216948528815371491ed58978dc5cb314b777e94180eb2180ec5fc6',
                  'ebopark_session': 'eyJpdiI6ImdFUXFBazlSbUUwbkpvb1FzRHlvUnc9PSIsInZhbHVlIjoiZ3NKYzBpWUVuemdqcE9PdHYyU1A3VE4rN05uMER5MnhmSEFhTSt0XC9hdGQ1ZlFxMGdNc1BhOElHV2ZHYXI0XC9TIiwibWFjIjoiMzM2NDJiMmY2YjcxYjRlMWMzN2JmNWM2ZTgyMjJiZTIwODFhZjA3ZDg5MDUwNTk4YmU4ZjUyYjZkYjZmYTg5YyJ9'}

    start_urls = ['http://cees.ebopark.com/merchant/list?park_code=&park_name=&name=&contact_phone=&contact=&page=1&_=1695005260916']

    csv_file_path = "merchant-all.csv"

    current_page = 1
    max_page = 130

    def start_requests(self):
        url = "http://cees.ebopark.com/merchant/list?park_code=&park_name=&name=&contact_phone=&contact=&page=%d&_=1695005260916"%(self.current_page)
        yield Request(url, headers=self.ebo_headers, cookies=self.ebo_cookie, callback=self.ebo_parse_page)

    def ebo_parse_page(self, response):
        data = response.json()
        code = data['code']
        current_page = data['data']['current_page']
        data_list = data['data']['data']
        print(f"============================> Code: {code}")
        print(f"============================> Current Page: {current_page}")
        write_header = not os.path.exists(self.csv_file_path)
        with open(self.csv_file_path, mode='a', newline='') as file:
            for index, item in enumerate(data_list):
                processed_item = {k: v if v is not None else '' for k, v in item.items()}
                print(processed_item)
                writer = csv.DictWriter(file, fieldnames=processed_item.keys())
                if write_header and current_page == 1 and index == 0:
                    writer.writeheader()
                writer.writerow(processed_item)
        if len(data_list) == 24:
            self.current_page += 1
            next_url = "http://cees.ebopark.com/merchant/list?park_code=&park_name=&name=&contact_phone=&contact=&page=%d&_=1695005260916"%(self.current_page)
            yield Request(next_url, headers=self.ebo_headers, cookies=self.ebo_cookie, callback=self.ebo_parse_page)

