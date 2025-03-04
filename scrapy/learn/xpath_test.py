# pip install lxml
# XPath 用法 http://www.w3school.com.cn/xpath/index.asp

# 导入 lxml 库的 etree 模块
from lxml import etree

# 解析 *.html 文件，返回节点树对象
html_selector = etree.parse("movies.html", etree.HTMLParser())

# 获取根节点 html 的元素
# (/) 代表其实位置
root = html_selector.xpath("/html")
print(root)

# 获取 title 元素
title = html_selector.xpath("/html/head/title")
print(title)

# text() 获取节点 title 的文本
title_name = html_selector.xpath("/html/head/title/text()")
print(title_name)

# 获取所有电影名称
# 电影名称的 <p> 节点相对根节点很远，如果逐层查找，XPath 表达式会很长。故使用(//)可以不考虑位置获取符合规则的子孙节点
movie_name = html_selector.xpath("//p/text()")    # "/html//div[@id='content']/h1/text()"
print(movie_name)
# ['1.肖申克的救赎', '2.霸王别姬']

# 获取网页的编码格式
meta = html_selector.xpath("//meta/@charset")
print(meta)

# 获取 div 的 id 属性值 & 使用 (..) 来通过子节点查找父节点
attr = html_selector.xpath("//h1/../@id")
print(attr)








