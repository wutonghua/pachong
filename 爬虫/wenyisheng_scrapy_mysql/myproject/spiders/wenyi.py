#!/usr/bin/python
# -*- coding: utf-8 -*-
# !/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from myproject.items import MyprojectItem


class WenYiSpider(scrapy.Spider):
	name = 'wenyi'
	start_urls = ['http://ask.39.net/browse/2225-2-%s.html' % p for p in range(1, 175)]

	def parse(self, response):
		for href in response.xpath('//p[@class="question-ask-title"]/a/@href'):
			full_url = response.urljoin(href.extract())
			print(full_url)
			yield scrapy.Request(full_url, callback=self.parse_question)

	def parse_question(self, response):
		print(response.xpath('//div[@class="ask_cont"]/div[1]/p/text()').extract())
		print(response.xpath('//div[@class="sele_all marg_top"]/div[1]/p/text()').extract())
		item=MyprojectItem()
		item['title']=response.xpath('//div[@class="ask_cont"]/div[1]/p/text()').extract()
		if item['title']:
			item['title']=item['title'][0]
		else:
			item['title']=''
		item['dafu1']=response.xpath('//div[@class="sele_all marg_top"]/p/text()').extract()
		if item['dafu1']:
			item['dafu1']=item['dafu1'][0]
		else:
			item['dafu1']=''
		item['dafu2']= response.xpath('//div[@class="sele_all"]/p/text()').extract()
		if item['dafu2']:
			item['dafu2']=item['dafu2'][0]
		else:
			item['dafu2']=''
		yield item
