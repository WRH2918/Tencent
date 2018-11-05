# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import pymysql
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from Tencent.items import TencentItem
from scrapy.conf import settings
import json
class TencentPipeline(object):
    def __init__(self):
        # self.f = open("tencent_pipelines.json","w")
        self.data_set = set()
        #连接数据库
        self.client = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '',
            db = 'scrapy',
            charset = 'utf8'
        )
        self.cur = self.client.cursor()
    def process_item(self, item, spider):
        data = item['positionLink']
        if data in self.data_set:
            raise DropItem("Duplicate item found: %s" % item)
        sql = """insert into tencentitem(positionName,positionType,positionLink,peopleNumber,workLocation,publishTime)
                  values (%s,%s,%s,%s,%s,%s)"""
        lis = (item['positionName'],item['positionType'],item['positionLink'],item['peopleNumber'],item['workLocation'],item['publishTime'])
        self.cur.execute(sql,lis)
        self.client.commit()
        # print(item)
        # content = json.dumps(dict(item),ensure_ascii=False)+",\n"
        # self.f.write(content)
        return item
    def clost_spiders(self,spider):
        # self.f.close()
        self.cur.close()
        self.client.close()