# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BlackwidowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImgItem(scrapy.Item):
    image_urls = Field()
    image_dir = Field()
    images = Field()
    image_paths = Field()