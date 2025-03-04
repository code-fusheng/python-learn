# 项目管道
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class QidianHotPipeline(object):
    def process_item(self, item, spider):
        if item["form"] == "连载":
            item["form"] = "LZ"
        else:
            item["form"] = "WJ"
        return item

# 作品 作者去重
class DuplicatesPipeline(object):
    def __init__(self):
        self.author_set = set()
    def process_item(self, item, spider):
        if item["author"] in self.author_set:
            # 抛弃重复的 Item 项
            raise DropItem("查找到重复姓名的项目: %s"%item)
        else:
            self.author_set.add(item['author'])
        return item

class SaveToTxtPipeline(object):
    # file_name = "hot.txt"
    @classmethod
    def from_crawler(cls, crawler):
        cls.file_name = crawler.settings.get("FILE_NAME", "hot2.txt")
        return cls()
    file = None
    # Spider 开启时，执行打开文件操作
    def open_spider(self, spider):
        # 以追加形式打开文件
        self.file = open(self.file_name, "a", encoding="utf-8")
    # 数据处理
    def process_item(self, item, spider):
        novel_str = item['name'] + "; " + item['author'] + "; " + item['type'] + "; " + item['form'] + "\n"
        # 将字符串写入文件
        self.file.write(novel_str)
        return item

    # 执行关闭文件操作
    def class_spider(self, spider):
        self.file.close()