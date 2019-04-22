# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from twisted.enterprise import adbapi
from qunar.items import *

class QunarPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = dict(
            host=crawler.settings['MYSQL_HOST'],
            db=crawler.settings['MYSQL_DBNAME'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASSWD'],
            port=crawler.settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert,item,spider)


    def _conditional_insert(self,conn,item,spider):
        if isinstance(item,CityItem):
            conn.execute("insert into city (city_id, city_name, province,city_region) values(%s, %s, %s,%s)",
                         (item['city_id'], item['city_name'], item['province'],item['city_region']))

        elif isinstance(item,attractionItem):
            conn.execute("insert into attraction2 (attraction_id, attraction_name, city_id,rank,des,time,"+\
                         "score,address,tel,open_time,ticket,season,traffic,comment_num"
                         ") values(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (item['attraction_id'], item['attraction_name'], item['city_id'], item['rank'],item['des'],
                          item['time'],item['score'],item['address'],item['tel'],item['open_time'],item['ticket'],
                          item['season'],item['traffic'],item['comment_num']))

        elif isinstance(item,hotelItem):
            conn.execute("insert into hotel2 (hotel_id, hotel_name, distance,score,attraction_id) values(%s, %s, %s,%s,%s)",
                         (item['hotel_id'], item['hotel_name'], item['distance'], item['score'],item['attraction_id']))

        elif isinstance(item,foodItem):
            conn.execute(
                "insert into food2 (food_id, food_name, distance,score,attraction_id) values(%s, %s, %s,%s,%s)",
                (item['food_id'], item['food_name'], item['distance'], item['score'], item['attraction_id']))

        elif isinstance(item,aroundAtt):
            conn.execute(
                "insert into aroundatt2 (aroundAtt_id, aroundAtt_name, distance,score,attraction_id) values(%s, %s, %s,%s,%s)",
                (item['aroundAtt_id'], item['aroundAtt_name'], item['distance'], item['score'], item['attraction_id']))

        else:
            conn.execute(
                "insert into shop2 (shop_id, shop_name, distance,score,attraction_id) values(%s, %s, %s,%s,%s)",
                (item['shop_id'], item['shop_name'], item['distance'], item['score'], item['attraction_id']))


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].insert(
            {'playListName': item.get('playListName'), 'playListAuthor': item.get('playListAuthor'),
             'song': item.get('song')})
        return item
