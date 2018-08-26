# -*- coding: utf-8 -*-
import scrapy

from blackwidow.items import ImgItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/147771']

    def parse(self, response):
        max_page_num = response.xpath('//div[@class="pagenavi"]/a/span/text()').extract()[-2]
        base_url = self.start_urls[0]
        for i in range(1, int(max_page_num) + 1):
            url = base_url + "/" + str(i)
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_img)


    def parse_img(self, response):
        img_urls = response.xpath('//div[@class="main-image"]//img/@src').extract()
        item = ImgItem()
        item['image_urls'] = img_urls
        yield item
