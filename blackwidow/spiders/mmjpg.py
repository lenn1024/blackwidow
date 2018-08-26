# -*- coding: utf-8 -*-
import scrapy

from blackwidow.items import ImgItem


class MmjpgSpider(scrapy.Spider):
    name = 'mmjpg'
    allowed_domains = ['mmjpg.com']
    start_urls = ['http://www.mmjpg.com/mm/1450']

    def parse(self, response):
        max_page = response.xpath('//div[@id="page"]/a/text()').extract()[-2]
        base_url = self.start_urls[0]
        for i in range(1, int(max_page) + 1):
            url = base_url + "/" + str(i)
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_img)

    def parse_img(self, response):
        print("===================")
        img_urls = response.xpath('//div[@id="content"]/a/img/@src').extract()
        print(img_urls)
        item = ImgItem()
        item['image_urls'] = img_urls
        yield item