# -*- coding: utf-8 -*-
import scrapy
from paper.items import SciRobIssueItem


class ScirobSpider(scrapy.Spider):
    name = 'scirob'
    base_url = "https://robotics.sciencemag.org/content/by/year/"
    start_year = 2016
    current_year = 2019

    custom_settings = {
        "DOWNLOAD_TIMEOUT": 300,
        # set the SciRobPdfsPipeline to the first handling pipeline when items are passed to the pipelines
        "ITEM_PIPELINES": {
            'paper.pipelines.SciRobPdfsPipeline': 1
        },
        'MEDIA_ALLOW_REDIRECTS': True,
        'FILES_STORE': "downloads",  # define where to store the files
        'FILES_EXPIRES': 120,
    }

    def start_requests(self):
        year_range = range(self.start_year, self.current_year + 1)
        for year in year_range:
            # generate the url for archive page of each year
            url = self.base_url + str(year)
            self.log(url)
            # request the archive page
            yield scrapy.Request(url, callback=self.parse_issue)

    # extract the url for each issue and request them
    def parse_issue(self, response):
        highlight_image_links = response.css("a.highlight-image-linked")
        for tag_a in highlight_image_links:
            yield response.follow(tag_a, callback=self.parse_pdf)

    # extract all urls for pdfs in the issue and store them in the item
    def parse_pdf(self, response):
        # extract the volume and issue
        current_url = response.url
        volume = int(current_url.split("/")[-2])
        issue = int(current_url.split("/")[-1])
        # extract urls of all pdf and store them in the item
        issue = SciRobIssueItem(volume=volume, issue=issue)
        tag_ul = response.css("ul.issue-toc.item-list")
        tags_a = tag_ul.css(
            "a.highwire-variant-link.variant-full-textpdf.link-icon")
        pdf_urls = []
        for tag_a in tags_a:
            pdf_url = response.urljoin(tag_a.css("a::attr(href)").get())
            # in fact, there is a url redirection here, autohandled by scrapy
            pdf_urls.append(pdf_url)
            issue["file_urls"] = pdf_urls
            # return the extracted data for pipeline for postprocessing
            yield issue
