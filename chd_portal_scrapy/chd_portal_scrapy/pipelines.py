# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class ChdPortalScrapyPipeline(object):
    def open_spider(self,spider):
        pass
    
    def close_spider(self,spider):
        pass
    def process_item(self, item, spider):
        return item

class BulletinPipeline(object):
    def __init__(self,host,database,user,password,port,table):
        self.host=host
        self.database=database
        self.user=user
        self.password=password
        self.port=port
        self.table=table

    @classmethod
    def from_crawler(cls,crawler):
        '''
        获取设置
        '''
        mysql_data=crawler.settings.get('MYSQL_DATA')
        return cls(
            host=mysql_data['host'],
            database=mysql_data['database'],
            user=mysql_data['user'],
            password=mysql_data['password'],
            port=mysql_data['port'],
            table=mysql_data['table']
        )

    def open_spider(self,spider):
        self.db=pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
        self.cursor=self.db.cursor()
    
    def close_spider(self,spider):
        self.db.close()

    
    def process_item(self, item, spider):
        
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql='insert into %s (%s) values (%s)' % (self.table,keys,values)
        try:
            self.cursor.execute(sql,tuple(data.values()))
            self.db.commit()
        except:
            self.db.rollback()
        return item