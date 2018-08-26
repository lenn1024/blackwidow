# -*- coding: utf-8 -*-
import scrapy

from blackwidow.items import ImgItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/146869']
    image_dir = 'full'

    def parse(self, response):
        # 读取图片title作为存储路径
        self.reset_image_dir(response)
        # 获取总页数
        max_page_num = response.xpath('//div[@class="pagenavi"]/a/span/text()').extract()[-2]
        # 根据base_url 构造 爬取链接
        base_url = self.start_urls[0]
        for i in range(1, int(max_page_num) + 1):
            url = base_url + "/" + str(i)
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_img)


    def parse_img(self, response):
        img_urls = response.xpath('//div[@class="main-image"]//img/@src').extract()
        item = ImgItem()
        item['image_urls'] = img_urls
        item['image_dir'] = self.image_dir
        yield item

    def reset_image_dir(self, response):
        self.image_dir = response.xpath('//h2[@class="main-title"]/text()').extract_first()