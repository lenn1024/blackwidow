# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from selenium import webdriver

from blackwidow.items import ImgItem


class Win4000Spider(scrapy.Spider):
    name = 'win4000'
    allowed_domains = ['www.win4000.com']
    start_urls = ['http://www.win4000.com/wallpaper_detail_149502.html']
    image_dir = 'win4000'

    def parse(self, response):
        page_urls = response.xpath('//ul[@id="scroll"]//a/@href').extract()
        for page_url in page_urls:
            yield scrapy.Request(url=page_url, callback=self.parse_img)
        pass

    def parse_img(self, response):
        img_urls = response.xpath('//div[@class="pic-meinv"]//img/@src').extract()

        item = ImgItem()
        item['image_dir'] = self.image_dir
        item['image_urls'] = img_urls
        yield item