import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from lianjia_home.items import LianjiaHomeItem

class HomeSpider(Spider):
    current_page = 1
    name = 'home'
    # allowed_domains = ['su.lianjia.com']
    # start_urls = ['http://su.lianjia.com/']
    def start_requests(self):
        url = "https://su.lianjia.com/ershoufang/"
        yield Request(url, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302] }, callback=self.lianjia_parse)
    def lianjia_parse(self, response):
        # XPath 定位二手房信息的 div 元素
        list_selector = response.xpath("//li/div[@class='info clear']")
        # 依次遍历 获取二手房名称、户型、面积、朝向等数据
        for item_selector in list_selector:
            try:
                # 获取房屋名称
                name = item_selector.xpath("div[@class='title']/a/text()").extract_first()
                # 获取其他信息
                other = item_selector.xpath("div[@class='houseInfo']/text()").extract_first()
                # 以 ｜ 作为间隔，转换为列表
                other_list = other.split("|")
                type = other_list[1].strip(" ")  # 户型
                area = other_list[2].strip(" ")  # 面积
                direction = other_list[3].strip(" ")  # 朝向
                fitment = other_list[4].strip(" ")  # 是否装修
                elevator = other_list[5].strip(" ")  # 有无电梯

                # 获取总价和单价 存入列表
                price_list = item_selector.xpath("div[@class='priceInfo']//span/text()")
                # 总价
                total_price = price_list[0].extract()
                # 单价
                unit_price = price_list[1].extract()

                item = LianjiaHomeItem()
                item['name'] = name.strip(" ")
                item['type'] = type
                item['area'] = area
                item['direction'] = direction
                item['fitment'] = fitment
                item['elevator'] = elevator
                item['total_price'] = total_price
                item['unit_price'] = unit_price
                print(item)
                # 获取详情页 URL
                # url = item_selector.xpath("div[@class='title']/a/@href").extract_first()
                # 详情页请求
                # yield Request(url, meta={"item": item,
                #                          'dont_redirect': True,
                #                          'handle_httpstatus_list': [301, 302]},
                #               callback=self.property_parse)
                yield item
            except:
                pass
        # if self.current_page == 1:
        #     self.total_page = response.xpath("//div[@class='page-box house-lst-page-box']//@page-data-v1").re("\d+")
        #     self.total_page = int(self.total_page[0])
        # self.current_page += 1
        # if self.current_page <= 2:
        #     next_url = "https://su.lianjia.com/ershoufang/pg%d"%(self.current_page)
        #     yield Request(next_url, callback=self.lianjia_parse)
    # 详情页解析函数
    def property_parse(self, response):
        # 1. 获取产权信息
        property = response.xpath("//div[@class='transaction']/div[@class='content']/ul/li[6]/text()").extract_first()
        # 2. 获取主页面中的房屋信息
        item = response.meta["item"]
        # 3. 将产权嘻嘻你添加到item中，返回给引擎
        item['property'] = property
        yield item
