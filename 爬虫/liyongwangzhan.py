#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get('http://www.120ask.com/list/xewk/')
page_info_first=browser.find_element_by_css_selector('.h-aa2')
#print(page_info_first.text)
for page in range(200):
	if page > 2:
		break
	url='http://www.120ask.com/list/xewk/all/' + str(page)
	browser.get(url)
	browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
	time.sleep(3)
	title=browser.find_element_by_css_selector('#list > div.h-left.fl > div.t13.h-main > ul > li:nth-child(2) > div.fl.h-left-p > p > a:nth-child(1)').text
	question=browser.find_element_by_css_selector('#list > div.h-left.fl > div.t13.h-main > ul > li:nth-child(2) > div.fl.h-left-p > p > a.q-quename').text
	links = browser.find_elements_by_tag_name("a")
	print(links)
	for link in links:
		if 'q-quename' in link.get_attribute("class") and ('padding-right:0' in link.get_attribute("style")):
			print(link)

			browser.get(link)
			answer1=browser.find_element_by_css_selector('#d_msCon > p.crazy_new').text
			answer2=browser.find_element_by_css_selector('#reply7690602 > p').text
			print(answer1,answer2)
		else:
			pass

