from scrapy import Request
from scrapy.spiders import Spider
from qidian_hot.items import QidianHotItem
from scrapy.loader import ItemLoader

class HotSalesSpider(Spider):
    # 定义爬虫名称 [必填项、唯一标识]
    name = "hot"
    # 设置用户代理（浏览器类型）
    # qidian_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    current_page = 1
    # 起始 URL 列表
    start_urls = ["https://www.qidian.com/rank/hotsales/page1"]
    # 请求函数 读取 URL 生成 Request 请求对象
    # def start_requests(self):
    def start_requests(self):
        url = "https://www.qidian.com/rank/hotsales/page1"
        yield Request(url, callback=self.qidian_parse)
    # 自定义解析函数
    def qidian_parse(self, response):
        # 使用 XPath 定位元素
        list_selector = response.xpath("//div[@class='book-mid-info']")
        print(list_selector)
        # 依次读取小说元素 获取 名称、作者、类型、形式
        for item_selector in list_selector:
            # 获取小说名称
            name = item_selector.xpath("h2/a/text()").extract_first()
            print(name)
            # 获取作者
            author = item_selector.xpath("p[1]/a[1]/text()").extract()[0]
            # 获取类型
            type = item_selector.xpath("p[1]/a[2]/text()").extract()[0]
            # 获取形式(连载/完本)
            form = item_selector.xpath("p[1]/span/text()").extract()[0]
            # 信息保存至字典
            # hot_dict = {
            #     "name": name,
            #     "author": author,
            #     "type": type,
            #     "form": form
            # }
            item = QidianHotItem()
            item["name"] = name
            item["author"] = author
            item["type"] = type
            item["form"] = form
            yield item
        #
        self.current_page += 1
        if self.current_page <= 2:
            next_url = "https://www.qidian.com/rank/hotsales/page%d"%(self.current_page)
            yield Request(next_url, callback=self.qidian_parse)
    def parse_for_css(self, response):
        list_selector = response.css("[class='book-mid-info']")
        for item_selector in list_selector:
            name = item_selector.css("h2>a::text").extract_first()
            author = item_selector.css(".author a::text").extract()[0]
            type = item_selector.css(".author a::text").extract()[1]
            form = item_selector.css(".author span::text").extract_first()
            hot_dict = {
                "name": name,
                "author": author,
                "type": type,
                "form": form
            }
            yield hot_dict
    # 解析函数
    def parse(self, response, **kwargs):
        # 使用 XPath 定位元素
        list_selector = response.xpath("//div[@class='book-mid-info']")
        # 依次读取小说元素 获取 名称、作者、类型、形式
        for item_selector in list_selector:
            # 获取小说名称
            name = item_selector.xpath("h2/a/text()").extract()[0]
            print(name)
            # 获取作者
            author = item_selector.xpath("p[1]/a[1]/text()").extract()[0]
            # 获取类型
            type = item_selector.xpath("p[1]/a[2]/text()").extract()[0]
            # 获取形式(连载/完本)
            form = item_selector.xpath("p[1]/span/text()").extract()[0]
            # 信息保存至字典
            hot_dict = {
                "name": name,
                "author": author,
                "type": type,
                "form": form
            }
            yield hot_dict

    def parse_for_itemloader(self, response):
        # 使用 XPath 定位元素
        list_selector = response.xpath("//div[@class='book-mid-info']")
        # 依次读取小说元素 获取 名称、作者、类型、形式
        for item_selector in list_selector:
            # ItemLoader
            novel = ItemLoader(item=QidianHotItem(), selector=item_selector)
            novel.add_xpath("name", "h2/a/text()")
            novel.add_xpath("author", "p[1]/a[1]/text()")
            novel.add_xpath("type", "p[1]/a[2]/text()")
            novel.add_css("form", ".author span::text")
            yield novel.load_item()