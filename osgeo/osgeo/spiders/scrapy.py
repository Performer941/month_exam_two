# -*- coding: utf-8 -*-
import re

import scrapy


class ScrapySpider(scrapy.Spider):
    name = 'scrapy'
    allowed_domains = ['osgeo.cn']
    start_urls = ['https://www.osgeo.cn/scrapy/intro/install.html']

    def parse(self, response):
        with open("index.html", "rb") as f:

            x0 = f.read()
            # print(x0)

            # css.js
            x1 = re.search("=\"../(.*?)\"", str(x0))
            print(x1)
            # if x1:
            #     self.parse(response)
            # else:
            #     print('获取结束')
