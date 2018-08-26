# -*- coding: utf-8 -*-
import scrapy

from blackwidow.items import ImgItem

# 图片下载器
# 设置图片URL -> download_images
class PicDownloaderSpider(scrapy.Spider):
    name = 'pic_downloader'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']
    download_images = ['http://upload-images.jianshu.io/upload_images/11212243-740f421de14ef5f2.jpg']
    image_dir = 'full'

    def parse(self, response):
        item = ImgItem()
        item['image_urls'] = self.download_images
        item['image_dir'] = self.image_dir
        yield item