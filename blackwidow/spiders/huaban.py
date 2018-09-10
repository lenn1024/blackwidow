# -*- coding: utf-8 -*-
import re

import scrapy
import json
from scrapy_splash import SplashRequest

from blackwidow.items import ImgItem


class HuabanSpider(scrapy.Spider):
    name = 'huaban'
    allowed_domains = ['huaban.com']
    # start_urls = ['http://huaban.com/boards/37953848/?jltb7rdb&max=1230203890&limit=182']
    start_urls = ['http://huaban.com/boards/14300460/'
                  # 'http://huaban.com/boards/46948705/',
                  # 'http://huaban.com/boards/46929901/',
                  # 'http://huaban.com/boards/46947831/',
                  # 'http://huaban.com/boards/43683315/',
                  # 'http://huaban.com/boards/46932906/',
                  # 'http://huaban.com/boards/42697872/',
                  # 'http://huaban.com/boards/46948154/',
                  # 'http://huaban.com/boards/46936103/',
                  # 'http://huaban.com/boards/46936800/',
                  # 'http://huaban.com/boards/46959338/'
                  ]

    root_path = 'http://huaban.com'
    image_dir = 'huaban'

    json_header = {
        "Accept": "application/json",
        'X-Request': 'JSON',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        # 封装splash request
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                                args={'wait': 1}, endpoint='render.html')

    def parse(self, response):
        max_pin = ''
        hrefs = response.xpath('//div[@id="waterfall"]//a/@href').extract()
        for href in hrefs:
            result = re.match(r'/pins/(\d+)/?', href)
            if result:
                url = self.root_path + href
                yield SplashRequest(url=url, callback=self.parse_detail,
                                args={'wait': 1}, endpoint='render.html')
                # 记录max_pin
                max_pin = result.group(1)

        # 构造json请求
        json_url = self.generateJsonUrl(max_pin)
        yield scrapy.Request(url=json_url, headers=self.json_header, callback=self.parse_json)

    def parse_json(self, response):
        data = json.loads(response.body)
        pins = data['board']['pins']
        if len(pins) > 0:
            for pin in pins:
                url = self.root_path + '/pins/' + str(pin['pin_id'])
                yield SplashRequest(url=url, callback=self.parse_detail,
                                    args={'wait': 1}, endpoint='render.html')
            # 继续构造json请求
            max_pin = pins[-1]
            json_url = self.generateJsonUrl(max_pin)
            yield scrapy.Request(url=json_url, headers=self.json_header, callback=self.parse_json)

    def parse_detail(self, response):
        print("###########")
        # title = response.xpath('//body/text()').extract_first()
        # print(response.xpath('//div[@id="baidu_image_holder"]//img/@src').extract_first())
        img_url = response.xpath('//div[@id="baidu_image_holder"]//img/@src').extract_first()
        img_urls = ['http:' + img_url]
        print("###########")

        # download img
        item = ImgItem()
        item['image_dir'] = self.image_dir
        item['image_urls'] = img_urls
        yield item

    # 构造json请求url
    def generateJsonUrl(self, max, limit=100):
        base_url = self.start_urls[0]
        json_url = base_url + '?jltb7rdb&max=' + str(max) + '&limit=' + str(limit)
        return json_url