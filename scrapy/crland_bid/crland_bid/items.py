# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrlandBidItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    type = scrapy.Field()
    pub_time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    attachment = scrapy.Field()
