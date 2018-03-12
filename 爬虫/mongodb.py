#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import time
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)                 # 连接Mongodb数据库
sense = client['sense']                                          # 创建数据库
url_list = sense['url_list']                                     # 创建数据表
item_info = sense['item_info']



def get_neike_urls():
    """获取首页所有儿科的url列表"""
    with open('neike.html',encoding='utf-8') as f:
        response = f.read()                                      # 读取本地html文件
    soup = BeautifulSoup(response, 'lxml')
    urls = soup.select('.h-ul1 > li > a')

    return [url.get('href') for url in urls]                     # 列表解析式，存储各疾病科URL链接


def get_page_list(neike, page=1):
    """获取列表页数据"""
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 创建时间
    url = 'http://www.120ask.com/list/%s/all/%s' % (neike.split('/')[-1], page)
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    response = requests.get(url,headers=headers)  # 发送请求
    # print(response.status_code)
    soup=BeautifulSoup(response.text,'lxml')
    title=soup.select('#list > div.h-left.fl > div.t13.h-main > ul > li > div.fl.h-left-p > p > a') #问题标题
    huidashu=soup.select('#list > div.h-left.fl > div.t13.h-main > ul > li > div.fr.h-right-p > span.h-span1') #回答数目
    # print(title,huidashu)
    for i in range(0,len(title)):
        wenti=title[i].get('title').strip()
        url=title[i].get('href').strip()
        huidashumu=huidashu[i].text

        data = {'wenti': wenti, 'huidashumu': huidashumu, 'url': url, 'create_time': now}
        url_list.insert_one(data)                                # 将数据插入数据库
        print(data)
def get_all_list(neike):
    #爬取多页码列表数据
    for page in range(0,200):
        get_page_list(neike,page)
def get_item_info(url):
    #获取详情页的数据
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text,'lxml')
    wentims=list(soup.select('#d_msCon > p.crazy_new')[0].stripped_strings)
    huida=list(soup.select('#reply > p')[0].stripped_strings)
    data = {'wentims': wentims, 'huida': huida, 'url': url}
    item_info.insert_one(data)


if __name__ == '__main__':
    # get_page_list('http://www.120ask.com/list/xesjnk')
    # print(get_neike_urls())
    # listing = [i['url'] for i in url_list.find()]
    neike_urls = get_neike_urls()
    pool = Pool(processes=3)                                     # 设置进程池中的进程数
    pool.map(get_all_list, neike_urls)                           # 将列表中的每个对象应用到get_page_list函数
    # pool.map(get_item_info, listing)
    pool.close()                                                 # 等待进程池中的进程执行结束后再关闭pool
    pool.join()                                                  # 防止主进程在子进程结束前提前关闭
