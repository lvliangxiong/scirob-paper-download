# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy.item import Field


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SciRobIssueItem(Item):
    volume = Field()
    issue = Field()
    # contain the urls of pdf
    file_urls = Field()
    # will be populated automatically after downloading
    files = Field()