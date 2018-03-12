#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy


class YouwenSpider(scrapy.Spider):
    name = 'youwennews'
    start_urls = ['http://www.120ask.com/list/xesjnk/']
    def parseurl(self, response):
        # 请求第一页
        yield scrapy.Request(response.url, callback=self.parse)

        # 请求其它页//*[@id="list"]/div[1]/div[3]/div[3]/span/a//*[@id="list"]/a
        for page in response.xpath('//*[@clears ="clears h-page"]/a'):
            link = page.xpath('@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse)
    def parse(self,response):
        for href in response.xpath('//*[@id="list"]/div/div/ul/li/div/p/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)
            
            
    def parse_question(self,response):
        print(response.xpath('//*[@id="body_main"]/div/div/div/div/div/span/text()').extract_first())
        print(response.xpath('//div[@class="b_askbox"]/div/h1/text()').extract_first())
        print(response.xpath('//*[@class="crazy_new"]/p/text()').extract())
		


        yield {
			'label':1,
			'keshi':'小儿矮小症',
			'nianling':((response.xpath('//*[@id="body_main"]/div/div/div/div/div/span/text()').extract_first())).split(' ')[2],
            'xiebie':((response.xpath('//*[@id="body_main"]/div/div/div/div/div/span/text()').extract_first())).split(' ')[0],
            'title': response.xpath('//div[@class="b_askbox"]/div/h1/text()').extract_first(),
            'zhenduan': response.xpath('//*[@class="crazy_new"]/p/text()').extract(),
        }