from scrapy import cmdline

cmdline.execute("scrapy crawl hot -o hot.csv".split())