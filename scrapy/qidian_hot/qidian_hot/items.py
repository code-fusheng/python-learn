# 数据实体
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
# 定义一个转换小说形式的函数
def form_convert(form):
    if form[0] == "连载":
        return "LZ"
    else:
        return "WJ"


class QidianHotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())   # 小说名称
    author = scrapy.Field(output_processor=TakeFirst()) # 作者
    type = scrapy.Field(output_processor=TakeFirst())   # 类型
    form = scrapy.Field(input_processor=form_convert, output_processor=TakeFirst())   # 形式
