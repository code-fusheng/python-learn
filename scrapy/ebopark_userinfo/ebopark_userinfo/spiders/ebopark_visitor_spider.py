import json
import csv
import os
import random

from scrapy import Request
from scrapy.spiders import Spider

class VisitorSpider(Spider):
    # 爬虫名称
    name = 'ebo_visitor'

    custom_settings = {
        'DOWNLOAD_DELAY': random.randint(2, 5),  # 设置请求间隔为1秒
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

    # 起始 url
    start_urls = ["http://cees.ebopark.com/visitorappointment?park_code=&name=&plate_number=&mobile=&master_name=&master_mobile=&start_time=&end_time=&park_name=&data_resource=&status=ALL&master_department=&page=1&_=1694849889608"]

    current_page = 1
    max_page = 130

    # plate_numbers = ['渝', '豫', '云', '辽', '吉', '黑', '湘', '鲁', '新', '苏', '浙', '赣',
    #                  '鄂', '粤', '桂', '甘', '晋', '蒙', '滇', '黔', '藏', '陕', '青', '宁',
    #                  '藏', '川', '台', '澳', '粤']
    # plate_numbers = ['浙', '赣', '鄂', '粤', '桂', '甘', '晋', '蒙', '滇', '黔', '藏', '陕', '青', '宁', '台', '澳']
    plate_numbers = ['苏', '川']
    plate_index = 0
    plate_number = plate_numbers[plate_index]

    csv_file_path = "visitor-%s.csv"%(plate_number)

    def start_requests(self):
        url = "http://cees.ebopark.com/visitorappointment?park_code=&name=&plate_number=%s&mobile=&master_name=&master_mobile=&start_time=&end_time=&park_name=&data_resource=&status=ALL&master_department=&page=%d&_=1694849889608"%(self.plate_number, self.current_page)
        yield Request(url, headers=self.ebo_headers, cookies=self.ebo_cookie, callback=self.ebo_parse_page)

    def ebo_parse(self, response):
        # print("===> response", response)
        data = response.json()
        # data = json.load(response)
        # print("===> data", data)
        code = data['code']
        current_page = data['data']['current_page']
        data_list = data['data']['data']

        print(f"============================> Code: {code}")
        print(f"============================> Current Page: {current_page}")

        write_header = not os.path.exists(self.csv_file_path)

        # 写入CSV文件
        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'qn', 'park_code', 'name', 'idcard', 'mobile', 'user_token', 'plate_number', 'master_name', 'master_department',
                                                      'master_room_no', 'master_mobile', 'garage', 'start_time', 'end_time', 'notes', 'status',
                                                      'data_resource', 'in_authority', 'out_authority', 'operator', 'created_at', 'updated_at', 'other_con'])
            # 写入表头
            if write_header:
                writer.writeheader()

            for item in data_list:
                # print(item)
                processed_item = {k: v if v is not None else '' for k, v in item.items()}
                # print(processed_item)
                writer = csv.DictWriter(file, fieldnames=processed_item.keys())
                writer.writerow(processed_item)


    def ebo_parse_page(self, response):
        # print("===> response", response)
        data = response.json()
        # data = json.load(response)
        # print("===> data", data)
        code = data['code']
        current_page = data['data']['current_page']
        data_list = data['data']['data']

        print(f"============================> Code: {code}")
        print(f"============================> Current Page: {current_page}")



        write_header = not os.path.exists(self.csv_file_path)

        # 写入CSV文件
        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'qn', 'park_code', 'name', 'idcard', 'mobile', 'user_token', 'plate_number', 'master_name', 'master_department',
                                                      'master_room_no', 'master_mobile', 'garage', 'start_time', 'end_time', 'notes', 'status',
                                                      'data_resource', 'in_authority', 'out_authority', 'operator', 'created_at', 'updated_at', 'other_con'])
            # 写入表头
            if write_header:
                writer.writeheader()

            for item in data_list:
                # print(item)
                processed_item = {k: v if v is not None else '' for k, v in item.items()}
                print(processed_item)
                writer = csv.DictWriter(file, fieldnames=processed_item.keys())
                writer.writerow(processed_item)
        # if self.current_page <= self.max_page and len(data_list) == 24:
        if len(data_list) == 24:
            self.current_page += 1
            next_url = "http://cees.ebopark.com/visitorappointment?park_code=&name=&plate_number=%s&mobile=&master_name=&master_mobile=&start_time=&end_time=&park_name=&data_resource=&status=ALL&master_department=&page=%d&_=1694849889608"%(self.plate_number, self.current_page)
            yield Request(next_url, headers=self.ebo_headers, cookies=self.ebo_cookie, callback=self.ebo_parse_page)
        elif self.plate_index != len(self.plate_numbers) - 1:
            self.plate_index += 1
            self.plate_number = self.plate_numbers[self.plate_index]
            self.current_page = 1
            self.csv_file_path = "visitor-%s.csv"%(self.plate_number)
            next_url = "http://cees.ebopark.com/visitorappointment?park_code=&name=&plate_number=%s&mobile=&master_name=&master_mobile=&start_time=&end_time=&park_name=&data_resource=&status=ALL&master_department=&page=%d&_=1694849889608"%(self.plate_number, self.current_page)
            yield Request(next_url, headers=self.ebo_headers, cookies=self.ebo_cookie, callback=self.ebo_parse_page)




