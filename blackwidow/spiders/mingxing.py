# -*- coding: utf-8 -*-
import scrapy

from blackwidow.items import ImgItem


class MingxingSpider(scrapy.Spider):
    name = 'mingxing'
    allowed_domains = ['www.mingxing.com']
    start_urls = ['http://www.mingxing.com/tuku/index/id/307782.html']
    image_dir = 'mingxing'

    def parse(self, response):
        img_urls = response.xpath('//div[@class="swiper-slide"]//img/@src').extract()

        item = ImgItem()
        item['image_dir'] = self.image_dir
        item['image_urls'] = img_urls
        yield item