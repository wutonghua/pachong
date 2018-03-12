# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from shanqi.items import ShanqiItem
class ShanqiPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            db='rengongzhineng',
            user='root',
            passwd='wujian',
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item,spider):
        if item.__class__ == ShanqiItem:
            try:
                self.cursor.execute("""insert into shanqi(nianling,xingbie,title,zhenduan) value (%s,%s,%s,%s)""",
                                    (str(item['nianling']),str(item['xingbie']),str(item['title']),str(item['zhenduan'])))
                self.connect.commit()
            except Exception as e:
                print(e)
        else:
            pass
        return item
