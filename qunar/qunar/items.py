# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    pass

"""
城市id、城市名称、所属省份、所属地区
"""
class CityItem(scrapy.Item):
    table_name = 'city'
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    province = scrapy.Field()
    city_region = scrapy.Field()


"""
景点id、景点名称、所属城市id、排名、简介、建议游玩时间、评分、地址、电话、开放时间、门票、
旅游时节、交通指南、旅游点评数量、5分点评数量、4分点评数量、3分点评数量、2分点评数量、1分点评数量、好评点评数量、中评点评数量、差评点评数量
"""
class attractionItem(scrapy.Item):
    table_name = 'attraction'
    attraction_id = scrapy.Field()
    attraction_name = scrapy.Field()
    city_id = scrapy.Field()
    rank = scrapy.Field()
    des = scrapy.Field()
    time = scrapy.Field()
    score = scrapy.Field()
    address = scrapy.Field()
    tel = scrapy.Field()
    open_time = scrapy.Field()
    ticket = scrapy.Field()
    season = scrapy.Field()
    traffic = scrapy.Field()
    comment_num = scrapy.Field()
    five_star = scrapy.Field()
    four_star = scrapy.Field()
    three_star = scrapy.Field()
    two_star = scrapy.Field()
    one_star = scrapy.Field()
    good_comment = scrapy.Field()
    medium_comment = scrapy.Field()
    bad_comment = scrapy.Field()


"""
酒店id、酒店名称、距离本景点距离、评分
"""
class hotelItem(scrapy.Field):
    tabel_name = 'hotel'
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    distance = scrapy.Field()
    score = scrapy.Field()
    attraction_id = scrapy.Field()

"""
餐厅id、餐厅名称、距离本景点距离、评分
"""
class foodItem(scrapy.Field):

    tabel_name = 'food'
    food_id = scrapy.Field()
    food_name = scrapy.Field()
    distance = scrapy.Field()
    score = scrapy.Field()
    attraction_id = scrapy.Field()

"""
景点id、景点名称、距离本景点距离、评分  
"""
class aroundAtt(scrapy.Field):

    table_name = 'aroundatt'
    aroundAtt_id = scrapy.Field()
    aroundAtt_name = scrapy.Field()
    score = scrapy.Field()
    distance = scrapy.Field()
    attraction_id = scrapy.Field()


"""
购物商场id、商场名称、距离本景点距离、评分 
"""
class shopItem(scrapy.Field):
    table_name = 'shop'
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    score = scrapy.Field()
    distance = scrapy.Field()
    attraction_id = scrapy.Field()


