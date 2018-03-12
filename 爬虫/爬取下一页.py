#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
class MingyiSpider(scrapy.Spider):
    name = 'mingyizaixian'
    start_urls = ['http://ask.myzx.cn/kid190.html']
    
    def parse(self,response):
        for href in response.xpath('//div[@class="media_list ask-all-text"]/ul/li/div/div[2]/a/@href'):
            full_url = response.urljoin(href.extract())
            print(full_url)
            yield scrapy.Request(full_url,callback=self.parse_question)
        page = response.xpath('//div[@class="pages_b"]/a/@href').extract()
        for url in page:
            if url is not None:
                next_page = 'http://ask.myzx.cn/' + url
                yield scrapy.Request(next_page,callback=self.parse)
    def parse_question(self,response):
        print(response.xpath('//*[@class="question row"]/div/span/text()').extract_first())
        print(response.xpath('//*[@id="main"]/div[2]/div[1]/div[1]/dl[1]/dd/text()').extract())
        print(response.xpath('//*[@class="answer_content"]/div[1]/p/text()').extract())


        yield {
			'label':1,
			'keshi':'小儿内科症',
            'xiebie':response.xpath('//*[@class="question row"]/div/span/text()').extract_first(),
            'title': response.xpath('//*[@id="main"]/div[2]/div[1]/div[1]/dl[1]/dd/text()').extract(),
            'zhenduan': response.xpath('//*[@class="answer_content"]/div[1]/p/text()').extract(),
        }