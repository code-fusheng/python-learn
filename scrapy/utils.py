# -*- coding: utf-8 -*-
class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie
    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict
if __name__ == "__main__":
    cookie = "acw_tc=0b3c7d8216948528815371491ed58978dc5cb314b777e94180eb2180ec5fc6; ebopark_session=eyJpdiI6ImdFUXFBazlSbUUwbkpvb1FzRHlvUnc9PSIsInZhbHVlIjoiZ3NKYzBpWUVuemdqcE9PdHYyU1A3VE4rN05uMER5MnhmSEFhTSt0XC9hdGQ1ZlFxMGdNc1BhOElHV2ZHYXI0XC9TIiwibWFjIjoiMzM2NDJiMmY2YjcxYjRlMWMzN2JmNWM2ZTgyMjJiZTIwODFhZjA3ZDg5MDUwNTk4YmU4ZjUyYjZkYjZmYTg5YyJ9"
    trans = transCookie(cookie)
    print(trans.stringToDict())
    # print("津".encode('unicode_escape'))
    plate_number = "xxx"
    print( "visitor-%s.csv" % (plate_number))