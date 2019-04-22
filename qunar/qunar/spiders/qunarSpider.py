# -*- coding: utf-8 -*-
import scrapy
from qunar.items import *
from scrapy import Spider, Request, FormRequest


class QunarspiderSpider(scrapy.Spider):
    name = 'qunarSpider'
    allowed_domains = ['travel.qunar.com']
    start_urls = ['http://travel.qunar.com/place/?from=header']

    def parse(self, response):
        print("_________________________")
        region_list = response.xpath("//*[@id='js_destination_recommend']/div[2]/div[1]/div[2]/dl")
        i = 1
        for item in region_list:
            current_region = item.xpath("./dt/text()").extract_first()
            print(current_region)
            province_list = item.xpath("./dd/div")
            for provinceItem in province_list:
                current_province = provinceItem.xpath("./div/span/text()").extract_first()
                if(current_province is not None):
                    current_province = current_province.split(":")[0]
                else:
                    current_province = "nan"
                print(current_province)
                city_list = provinceItem.xpath("./ul/li")
                for cityItem in city_list:
                    city_name = cityItem.xpath("./a/text()").extract_first()
                    city_url = cityItem.xpath("./a/@href").extract_first()
                    cityitem = CityItem()
                    cityitem['city_name'] = city_name
                    cityitem['province'] = current_province
                    cityitem['city_region'] = current_region
                    cityitem['city_id'] = city_url.split('/')[-1].split('-')[1]
                    i += 1
                    # print(city_url, city_name, cityitem['city_id'])
                    # yield (cityitem)
                    yield Request(city_url + "-jingdian", meta={'city_id': cityitem['city_id'],
                                                                'city_url': city_url + "-jingdian"
                                                                }, callback=self.parse_attractionurl)

    def parse_attractionurl(self, response):

        city_id = response.meta['city_id']
        city_url = response.meta['city_url']
        atrraction_list = response.xpath("/html/body/div[2]/div/div[6]/div[1]/div/div[2]/ul/li")

        for attractionItem in atrraction_list:
            attraction_url = attractionItem.xpath("./a/@href").extract_first()
            attraction_id = attraction_url.split("/")[-1].split("-")[1]
            print("attraction_id",attraction_id)
            yield Request(attraction_url, meta={
                'city_id': city_id,
                'attraction_id': attraction_id,
                'attraction_url': attraction_url
            }, callback=self.parse_attraction_detail)

        flag = 0
        url = " "
        page_num_list = response.xpath("/html/body/div[2]/div/div[6]/div[1]/div/div[3]/a")
        if (len(page_num_list) >= 3):
            page_num = page_num_list[-2].xpath("./text()").extract_first()
            print("page_num", page_num)
            city_url_split = city_url.split("/")[-1].split("-")
            if (len(city_url_split) == 4):
                url = city_url + "-1-2"
            elif (int(city_url_split[-1]) < 100 and int(city_url_split[-1]) < int(page_num)):
                # print("city_url_split[-1]", city_url_split[-1])
                cutlist = city_url.split("-")[:-1]
                url = "-".join(cutlist) + "-" + str(int(city_url_split[-1]) + 1)
            else:
                flag = 1
                print(city_id, "done!")

        else:
            flag = 1

        if (flag == 0):
            # print(url)
            yield Request(url, meta={
                'city_id': city_id,
                'city_url': url
            }, callback=self.parse_attractionurl)

    def parse_attraction_detail(self, response):

        # print(response.body)
        attraction_url = response.meta['attraction_url']
        # print("attraction_url",attraction_url)
        att = attractionItem()
        att['city_id'] = response.meta['city_id']
        att['attraction_id'] = response.meta['attraction_id']
        att['attraction_name'] = response.xpath("//*[@id='js_mainleft']/div[3]/h1/text()").extract_first()
        att['score'] = response.xpath(
            "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[1]/span[1]/text()").extract_first()
        if att['score'] is None:
            att['score'] = 'nan'
        att['des'] = response.xpath("//*[@id='gs']/div[1]/p[1]/text()").extract_first()
        if att['des'] is None:
            att['des'] = 'nan'
        att['rank'] = response.xpath(
            "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[2]/div[1]/span/text()").extract_first()
        if att['rank'] is None:
            att['rank'] = 'nan'
        if response.xpath(
                "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[2]/div[2]/text()").extract_first() is None:
           att['time'] = 'nan'
        else:
            att['time'] = \
                response.xpath(
                    "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[2]/div[2]/text()").extract_first().split("：")[
                    -1]
        # print("time",att['time'])
        att['comment_num'] = response.xpath("//*[@id='more_cmt_href']/text()").extract_first()
        if att['comment_num'] is None:
            att['comment_num'] = 'nan'
        att['address'] = response.xpath(
            "//*[@id='gs']/div[2]/div/table/tr/td[1]/dl[1]/dd/span/text()").extract_first()
        if att['address'] is None:
            att['address'] = 'nan'
        att['tel'] = response.xpath(
            "//*[@id='gs']/div[2]/div/table/tr/td[1]/dl[2]/dd/span/text()").extract_first()
        if att['tel'] is None:
            att['tel'] = 'nan'
        att['open_time'] = response.xpath(
            "//*[@id='gs']/div[2]/div/table/tr/td[2]/dl/dd/span/p/text()").extract_first()
        # print('open_time',att['open_time'])
        # # print(response.xpath(
        # #     "//table"))
        if att['open_time'] is None:
            att['open_time'] = 'nan'
        att['ticket'] = response.xpath("//*[@id='mp']/div[2]/p/text()").extract_first()
        if att['ticket'] is None:
            att['ticket'] = 'nan'
        att['season'] = response.xpath("//*[@id='lysj']/div[2]/p/text()").extract_first()
        if att['season'] is None:
            att['season'] = 'nan'
        traffic1 = response.xpath("//*[@id='jtzn']/div[2]/p[2]/text()").extract_first()
        traffic2 = response.xpath("//*[@id='jtzn']/div[2]/p[5]/text()").extract_first()
        if traffic1 is None and traffic2 is None:
            att['traffic'] = 'nan'
        elif traffic2 is None:
            att['traffic'] = traffic1
        elif traffic1 is None:
            att['traffic'] = traffic2
        else:
            att['traffic'] = traffic1+" "+traffic2


        # todo 评价数量
        # yield Request(attraction_url + "?rank=1#lydp", meta={"item": att, "url": attraction_url},
        #               callback=self.parse_goodComment)
        yield (att)

        around_list = response.xpath("//*[@id='idContBox']/ul[1]/li")[:-1]
        for item in around_list:
            around = aroundAtt()
            around['aroundAtt_name'] = item.xpath("./div[1]/a/text()").extract_first()
            around['aroundAtt_id'] = item.xpath("./div[1]/a/@href").extract_first().split('/')[-1].split('-')[1]
            around['distance'] = item.xpath("./div[2]/span[2]/text()").extract_first()
            around['attraction_id'] = att['attraction_id']
            around['score'] = 'nan'
            if around['distance'] is None:
                around['distance'] = 'nan'
            yield (around)
            # around_url = item.xpath("./div[1]/a/@href").extract_first()
            # print("around_url-------------",around_url)
            # yield Request(around_url, meta={
            #     'attraction_id': att['attraction_id'],
            #     'distance': distance,
            #     'around_url': around_url
            # }, callback=self.parse_aroundAtt)

        food_list = response.xpath("//*[@id='idContBox']/ul[2]/li")[:-1]
        for item in food_list:
            food = foodItem()
            food['food_name'] = item.xpath("./div[1]/a/text()").extract_first()
            food['food_id'] = item.xpath("./div[1]/a/@href").extract_first().split('/')[-1].split('-')[1]
            food['distance']= item.xpath("./div[2]/span[2]/text()").extract_first()
            food['attraction_id'] = att['attraction_id']
            food['score'] = 'nan'
            if food['distance'] is None:
                food['distance'] = 'nan'
            yield(food)
            # food_url = item.xpath("./div[1]/a/@href").extract_first()
            # yield Request(food_url, meta={
            #     'attraction_id': att['attraction_id'],
            #     'distance': distance,
            #     'food_url': food_url
            # }, callback=self.parse_aroundfood)

        hotel_list = response.xpath("//*[@id='idContBox']/ul[3]/li")[:-1]
        for item in hotel_list:
            hotel = hotelItem()
            hotel['hotel_name'] = item.xpath("./div[1]/a/text()").extract_first()
            hotel['hotel_id'] = item.xpath("./div[1]/a/@href").extract_first().split('/')[-1].split('-')[1]
            hotel['distance'] = item.xpath("./div[2]/span[2]/text()").extract_first()
            hotel['attraction_id'] = att['attraction_id']
            hotel_url = item.xpath("./div[1]/a/@href").extract_first()
            # hotel['hotel_id'] = hotel_url.split('/')[2].split('_')[0] + hotel_url.split('/')[-1].split('?')[0].split('-')[-1]
            hotel['score'] = 'nan'
            if hotel['distance'] is None:
                hotel['distance'] = 'nan'
            yield(hotel)
            # yield Request(hotel_url, meta={
            #     'attraction_id': att['attraction_id'],
            #     'distance': distance,
            #     'hotel_url': hotel_url
            # }, callback=self.parse_aroundhotel)

        shop_list = response.xpath("//*[@id='idContBox']/ul[4]/li")[:-1]
        for item in shop_list:
            shop = shopItem()
            shop['shop_name'] = item.xpath("./div[1]/a/text()").extract_first()
            shop['shop_id'] = item.xpath("./div[1]/a/@href").extract_first().split('/')[-1].split('-')[1]
            shop['distance'] = item.xpath("./div[2]/span[2]/text()").extract_first()
            shop['attraction_id'] = att['attraction_id']
            shop['score'] = 'nan'
            if shop['distance'] is None:
                shop['distance'] = 'nan'
            yield(shop)
            # shop_url = item.xpath("./div[1]/a/@href").extract_first()
            # yield Request(shop_url, meta={
            #     'attraction_id': att['attraction_id'],
            #     'distance': distance,
            #     'shop_url': shop_url
            # }, callback=self.parse_aroundShop)

    def parse_goodComment(self, response):

        page_num = response.xpath("//*[@id='js_replace_box']/div[2]/div/a")[-2].xpath("./text()").extract_first()

        # yield Request(attraction_url + "?rank=2#lydp", )

    def parse_mediumComment(self, response):
        pass

    def parse_lowComment(self, response):
        pass

    def parse_aroundAtt(self, response):

        around = aroundAtt()
        around['attraction_id'] = response.meta['attraction_id']
        around['aroundAtt_name'] = response.xpath("//*[@id='js_mainleft']/div[3]/h1/text()").extract_first()
        around['score'] = response.xpath(
            "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[1]/span[1]/text()").extract_first()
        around['aroundAtt_id'] = response.meta['around_url'].split('/')[-1].split('-')[1]
        around['distance'] = response.meta['distance']
        if around['distance'] is None:
            around['distance'] = 'nan'
        if around['score'] is None:
            around['score'] = 'nan'
        yield (around)

    def parse_aroundShop(self, response):

        shop = shopItem()
        shop['distance'] = response.meta['distance']
        shop['shop_id'] = response.meta['shop_url'].split('/')[-1].split('-')[1]
        shop['attraction_id'] = response.meta['attraction_id']
        shop['shop_name'] = response.xpath("//*[@id='js_mainleft']/div[3]/h1/text()").extract_first()
        shop['score'] = response.xpath(
            "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[1]/span[1]/text()").extract_first()
        if shop['distance'] is None:
            shop['distance'] = 'nan'
        if shop['score'] is None:
            shop['score'] = 'nan'
        yield (shop)

    def parse_aroundfood(self, response):

        food = foodItem()
        food['distance'] = response.meta['distance']
        food['food_id'] = response.meta['food_url'].split('/')[-1].split('-')[1]
        food['attraction_id'] = response.meta['attraction_id']
        food['food_name'] = response.xpath("//*[@id='js_mainleft']/div[3]/h1/text()").extract_first()
        food['score'] = response.xpath(
            "//*[@id='js_mainleft']/div[4]/div/div[2]/div[1]/div[1]/span[1]/text()").extract_first()
        if food['distance'] is None:
            food['distance'] = 'nan'
        if food['score'] is None:
            food['score'] = 'nan'
        yield (food)

    def parse_aroundhotel(self, response):

        url = response.meta['hotel_url']
        hotel = hotelItem()
        hotel['hotel_name'] = response.xpath("//*[@id='hotelBaseinfo']/div[1]/div/h1/span[1]/text()").extract_first()
        hotel['distance'] = response.meta['distance']
        hotel['attraction_id'] = response.meta['attraction_id']
        hotel['score'] = response.xpath("//*[@id='headerUgc']/div/p[1]/span[1]/em/text()").extract_first()
        hotel['hotel_id'] = url.split('/')[2].split('_')[0] + url.split('/')[-1].split('?')[0].split('-')[-1]
        if hotel['distance'] is None:
            hotel['distance'] = 'nan'
        if hotel['score'] is None:
            hotel['score'] = 'nan'
        yield (hotel)
