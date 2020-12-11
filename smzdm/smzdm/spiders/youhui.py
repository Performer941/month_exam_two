# -*- coding: utf-8 -*-
import re

import scrapy


class YouhuiSpider(scrapy.Spider):
    name = 'youhui'
    allowed_domains = ['m.smzdm.com', 'm.smzdmio.com']
    start_urls = ['https://m.smzdm.com/youhui/']

    def parse(self, response):
        # 获取大框架
        x0 = response.xpath("//ul[@class='card-group-ul clearfix']/li[@class='card-group-list']")
        for item in x0:
            # 创建存放数据的字典
            dict01 = dict()
            # 标题
            x1 = item.xpath(".//div[@class='card-title']/text()").extract_first()
            str_x101 = str(x1).replace("['", "")
            str_x102 = str_x101.replace("']", "")
            str_x103 = str_x102.strip()

            # print(str_x103)

            # 价格包括折扣（分几步取）(价格)（是否包邮）（优惠）
            x2 = item.xpath(".//div[@class='card-price']/text()").extract_first()
            str_x201 = str(x2).replace("['", "")
            str_x202 = str_x201.replace("']", "")
            str_x203 = str_x202.strip()
            # 价格
            str_x203_1 = str_x203.split("元")[0]

            # print(str_x203_1)
            # 是否包邮
            # 验证是否有包邮的数据
            if str_x203.count("元"):
                str_x203_2 = str_x203.split("元")[1]
                str_x203_3 = str_x203_2.split("（")[0]
                # print(str_x203_3)
            else:
                # 如果没有此数据就为None
                str_x203_3 = None

            # 优惠
            # 验证是否有优惠的数据
            if str_x203.count("（"):
                str_x203_4 = str_x203.split("（")[1]
                str_x203_5 = str_x203_4.replace("）", "")
            else:
                # 如果没有此数据就为None
                str_x203_5 = None

            # 来源
            x3 = item.xpath(".//div[@class='card-actions-left']/span/span[1]/text()").extract_first()
            str_x301 = str(x3)

            # print(str_x301)

            # 上架日期
            x4 = item.xpath(".//div[@class='card-actions-left']/span/span[2]/text()").extract_first()
            str_x401 = str(x4)
            # print(str_x401)

            # 将数据写入字典方便存入mangodb
            dict01["标题"] = str_x103
            dict01["价格"] = str_x203_1
            dict01["是否包邮"] = str_x203_3
            dict01["优惠"] = str_x203_5
            dict01["来源"] = str_x301
            dict01["上架日期"] = str_x401

            yield dict01

        # 遍历路径页数
        for i in range(1, 51):
            next_page_url = "https://m.smzdm.com/youhui/p%d/" % i
            # 重新请求parse函数获取数据
            yield scrapy.Request(url=next_page_url, callback=self.parse)

