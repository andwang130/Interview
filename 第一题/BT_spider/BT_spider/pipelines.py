# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from BT_spider.settings import MYSQL_USER,MYSQL_DATABASE,MYSQL_HOST,MYSQL_PASSWD,MYSQL_PORT

class BtSpiderPipeline(object):
    def __init__(self):
        self.db=pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWD,database=MYSQL_DATABASE,port=MYSQL_PORT,charset='utf8')
        self.cursor=self.db.cursor()
    def process_item(self, item, spider):
        sql='INSERT INTO wp_posts(ID,post_content,post_title)VALUES(%s,%s,%s)'
        self.cursor.execute(sql,(item['ID'],item['conten'],item['title']))
        try:
            self.db.commit()
        except:
            self.db.rollback()
    def close_spider(self):#管道文件结束的时候执行的方法
        self.cursor.close()
        self.db.close()