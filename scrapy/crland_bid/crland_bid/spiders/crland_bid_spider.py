from scrapy import Request
from scrapy.spiders import Spider
from crland_bid.items import CrlandBidItem

class CrlandBidSipder(Spider):
    name = "crland_bid"
    allowed_domains = ['cbu.crland.com.cn']
    qidian_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    current_page = 1
    def start_requests(self):
        url = "https://cbu.crland.com.cn/bidding_msg/index.html"
        yield Request(url, meta={
                'dont_redirect': True,
                'If-None-Natch':'',
                'If-Modified-Since':'' }, callback=self.crland_parse)
    def crland_parse(self, response):
        list_selector = response.xpath("//td[@class='tender-title']")
        print(list_selector)
        for item_selector in list_selector:
            title = item_selector.xpath("a/text()").extract_first()
            status = item_selector.xpath("../td[3]/text()").extract_first()
            type = item_selector.xpath("../td[4]/text()").extract_first()
            pub_time = item_selector.xpath("../td[5]/text()").extract_first()
            item = CrlandBidItem()
            item["title"] = title
            item['status'] = status if status is not None else ""
            item['type'] = type if type is not None else ""
            item['pub_time'] = pub_time if pub_time is not None else ""
            # 处理详情页内容
            url = item_selector.xpath("a/@data-v1-href").extract_first()
            item['url'] = url
            yield Request(url, meta={"item":item}, callback=self.crland_detail_parse)
        self.current_page += 1
        if self.current_page <= 10:
            next_url = "https://cbu.crland.com.cn/bidding_msg/index_%d.html"%(self.current_page)
            yield Request(next_url, callback=self.crland_parse)
    def crland_detail_parse(self, response):
        item = response.meta["item"]
        full_title = response.xpath("//div[@class='east-news-detail-title']/text()").extract_first()
        content = response.xpath("//div[@class='east-news-detail-bottom']//span/text()").extract()
        item["title"] = full_title
        item["content"] = "+".join(content)
        yield item

