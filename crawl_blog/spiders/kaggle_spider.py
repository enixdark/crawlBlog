# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider , Rule
from scrapy.selector import Selector
# from html5print import HTMLBeautifier
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from bs4 import BeautifulSoup, Comment
from ..items import CrawlBlogItem
import sys

from scrapy.http import HtmlResponse
from scrapy.conf import settings

class KaggleSpider(CrawlSpider):
	name = "kaggle"
	allowed_domains = [
		"blog.kaggle.com",
	]

	start_urls = [
		'http://blog.kaggle.com',
	]

	__queue = []

	rules = [
	    Rule(LinkExtractor(allow=[], deny=__queue,
		restrict_xpaths=[
		'//*[@class="back-link"]',
		'//*[@class="post clearfix"]/h1/a[1]',
		# '//?page=\d+',
		# '//\w+/\w+/\w+/w+'
		]), callback='parse_extract_data', follow=True)]


	def parse_extract_data(self, response):

		if response.xpath('//*[@class="back-link"]') and 'Bandwidth exceeded' in response.body:
			raise CloseSpider('Exit')
		item = CrawlBlogItem()
		res = Selector(response)
		# import ipdb; ipdb.set_trace()
# 		title = res.xpath('//*[@id="ctl01"]/div[5]/div[3]/div/div[1]/div[2]/div/div[1]/div[2]/h1/text()').extract()
# 		item['title'] = ''.join(title).strip()
# 		
		item['author'] = ''.join(response.xpath('//span[@class="author vcard"]/a/text()').extract())
		item['name'] = ''.join(response.xpath('//div[@class="article-header-inside"]/h1/text()').extract())
		
		date_time = ''.join(response.xpath('//span[@class="entry-date"]/a[2]/@href').extract())
		if date_time:
			item['datetime'] = date_time[-11:]

		item['url'] = response.url
		
		content = enumerate(response.xpath('//div[@class="entry-content"]/node()'))
		content_data = {}
		check_point = 'Summary'

		for index,data in content:
			_data = data.extract()
			if check_point not in content_data:
				content_data[check_point] = []
			if '<p>' in _data or '\n' in _data or 'attachment' in _data:
				content_data[check_point].append(data.extract())
			if '<h2>' in _data:
				check_point = BeautifulSoup(_data).text

		item['content'] = content_data

		if 'name' in item and item['name']:
			return item


