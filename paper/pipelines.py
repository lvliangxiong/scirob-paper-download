# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline
import os
from urllib.parse import urlparse


class PaperPipeline(object):
    def process_item(self, item, spider):
        return item


class SciRobPdfsPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        # get the index of pdf according to the position of url in the file_urls
        volume = item.get("volume", "NA")
        issue = item.get("issue", "NA")
        return [
            scrapy.Request(x,
                           meta={
                               "volume": volume,
                               "issue": issue,
                               "index": index + 1
                           })
            for index, x in enumerate(item.get(self.files_urls_field, []))
        ]

    def file_path(self, request, response=None, info=None):
        volume = request.meta.get("volume")
        issue = request.meta.get("issue")
        index = request.meta.get("index")
        # By default the file_path() method returns full/<request URL hash>.<extension>.
        # change the default path
        filename = ("[" + str(index) + "] " +
                    os.path.basename(urlparse(request.url).path))
        return "Volume %s Issue %s/%s" % (volume, issue, filename)
