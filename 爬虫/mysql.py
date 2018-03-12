#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import time
import pymysql as sql
from multiprocessing import Pool

def get_neike_urls(page):
    """获取首页所有儿科的url列表"""
    url = 'http://www.120ask.com/list/xesjkfk/all/%s' % page                                    # 读取本地html文件
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    response = requests.get(url, headers=headers)  # 发送请求
    soup = BeautifulSoup(response.text, 'lxml')
    urls = soup.select('#list > div.h-left.fl > div.t13.h-main > ul > li > div.fl.h-left-p > p > a')
    # 列表解析式，存储各疾病科URL链接
    dizhi_list=[]
    for url in urls:
        dizhi_list.append(url.get('href'))
    insert_url_list(dizhi_list)
    return dizhi_list
def insert_url_list(dizhi_list):
    sql_host='localhost'
    sql_user='root'
    sql_pass='wujian'
    sql_name='rengongzhineng'
    con=sql.connect(host=sql_host, user=sql_user, passwd=sql_pass, db=sql_name,use_unicode=True, charset="utf8")
    column_str = """ url"""
    insert_str = ("%s, " * 1)[:-2]
    final_str = 'INSERT INTO dizhi (%s) VALUES (%s)' % (column_str, insert_str)
    with con:
        cur = con.cursor()
        cur.executemany(final_str, dizhi_list)
def get_page_list(neike, page):
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
    yemianItem=[]
    for i in range(0,len(title)):
        wenti=title[i].get('title').strip()
        url=title[i].get('href').strip()
        huidashumu=huidashu[i].text
        yemianItem.append((wenti, url, huidashumu))


    insert_page_list(yemianItem)
    return yemianItem

# def insert_page_list(yemianItem):
#     sql_host='localhost'
#     sql_user='root'
#     sql_pass='wujian'
#     sql_name='rengongzhineng'
#     con=sql.connect(host=sql_host, user=sql_user, passwd=sql_pass, db=sql_name,use_unicode=True, charset="utf8")
#     column_str = """wenti, url, huidashumu"""
#     insert_str = ("%s, " * 3)[:-2]
#     final_str = 'INSERT INTO erkeneike (%s) VALUES (%s)' % (column_str, insert_str)
#     with con:
#         cur = con.cursor()
#         cur.executemany(final_str, yemianItem)

def get_all_list():
    #爬取多页码列表数据
    for page in range(0, 200):
        get_neike_urls(page)

def get_all_itemurl():
    sql_host = 'localhost'
    sql_user = 'root'
    sql_pass = 'wujian'
    sql_name = 'rengongzhineng'
    con = sql.connect(host=sql_host, user=sql_user, passwd=sql_pass, db=sql_name, use_unicode=True, charset="utf8")
    with con:
        cur=con.cursor()
        cur.execute("select * from dizhi")
        results = cur.fetchall()
        for ii in results:
            print(ii)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            response = requests.get(ii[0], headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            wentims = soup.select('#d_askH1')
            huida2 = soup.select('#body_main > div.b_cont.t10.m1010.clears > div.b_left.fl.t10 > div.b_answerbox.t10')
            huida1 = soup.select('#body_main > div.b_cont.t10.m1010.clears > div.b_left.fl.t10 > div.b_answerbox.t10 > div > div.b_answercont.clears > div.b_anscontc > div.b_anscont_cont')
            print( wentims)
            items_url = []
            items_url.append((wentims, huida1, huida2))
        column_str = """wentims, huida1, huida2"""
        insert_str = ("%s, " * 3)[:-2]
        final_str = 'INSERT INTO dizhilist (%s) VALUES (%s)' % (column_str, insert_str)
        cur.executemany(final_str, items_url)


# def get_item_info(url):
#     #获取详情页的数据
#     # print(url)
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
#     response=requests.get(url,headers=headers)
#     soup=BeautifulSoup(response.text,'lxml')
#     wentims = soup.select('#d_msCon > p.crazy_new')[0].text
#     huida2 = soup.select('#body_main > div.b_cont.t10.m1010.clears > div.b_left.fl.t10 > div.b_answerbox.t10')[0].text
#     huida1=soup.select('#body_main > div.b_cont.t10.m1010.clears > div.b_left.fl.t10 > div.b_answerbox.t10 > div > div.b_answercont.clears > div.b_anscontc > div.b_anscont_cont')[0].text
#     items_url=[]
#     items_url.append((wentims,huida1,huida2))



if __name__ == '__main__':

    # listing = [i['url'] for i in url_list.find()]
    # neike_urls = get_neike_urls()
    # print(neike_urls)
    # pool = Pool(processes=5)                                     # 设置进程池中的进程数
    # pool.map(get_all_list, neike_urls)                           # 将列表中的每个对象应用到get_page_list函数
    # # pool.map(get_item_info, listing)
    # pool.close()                                                 # 等待进程池中的进程执行结束后再关闭pool
    # pool.join()
    # 防止主进程在子进程结束前提前关闭
    # get_all_list()
    # get_all_itemurl()
    get_all_itemurl()


