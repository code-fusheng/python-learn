# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrlandBidPipeline:
    def process_item(self, item, spider):
        return item

class SaveToTxtPipeline(object):
    # file_name = "bid.txt"
    @classmethod
    def from_crawler(cls, crawler):
        cls.file_name = "bid.txt"
        return cls()
    file = None
    # Spider 开启时，执行打开文件操作
    def open_spider(self, spider):
        # 以追加形式打开文件
        self.file = open(self.file_name, "a", encoding="utf-8")
    # 数据处理
    def process_item(self, item, spider):
        novel_str = item['title'] + "; " + item['url'] + "; " + item['status'] + "; " + item['type'] + "; " + item['pub_time'] + "\n"
        # 将字符串写入文件
        self.file.write(novel_str)
        return item

    # 执行关闭文件操作
    def class_spider(self, spider):
        self.file.close()
