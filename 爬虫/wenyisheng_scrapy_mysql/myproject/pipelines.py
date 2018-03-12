# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from myproject.items import MyprojectItem
class MyprojectPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            db='wenyi',
            user='root',
            passwd='wujian',
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == MyprojectItem:
            try:
                self.cursor.execute("""insert into xiaoer_ganmao(title,dafu1,dafu2) value (%s,%s,%s)""",
                                    (str(item['title']), str(item['dafu1']), str(item['dafu2'])))

                self.connect.commit()
            except Exception as e:
                print(e)
        else:
            pass
        return item
