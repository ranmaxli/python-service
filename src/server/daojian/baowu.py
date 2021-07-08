#! /user/bin/env python
# -*- coding: utf-8 -*

# 名称：获取低价宝物网商品基本信息
# 时间：2021-2-16 17:01:37
# 作者：ranmaxli

#  http://www.baowu.com/


#导包
from time import time
import urllib.request
from bs4 import BeautifulSoup
from decimal import Decimal
import re


#全局变量
global page_num
global page_max


# 模拟IE9发送请求
def load_page(url):
    user_agent = 'Mozilla/5.0(compatible;MSIE 9.0;Windows NT 6.1;Trident/5.0;'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)
    resopnse = urllib.request.urlopen(req)
    html = resopnse.read()
    return html.decode()


# 获取商品的所有信息
def get_goods_info(tables):
    global page_num
    global page_max

    for table in tables:

        # 库存
        goods_is_null = table.find('a', class_='btn05')
        if "立即购买" in str(goods_is_null):

            # 价格
            goods_price = table.find('strong', class_='orange')
            pattern = re.compile(r"<strong class=\"orange\">￥(.*?)</strong>", re.S)
            goods_price = pattern.findall(str(goods_price))
            for item in goods_price:
                goods_price = str(item)

            # 商品名称
            goods_url = ''
            goods_name = table.find('a', class_='blue1')
            pattern = re.compile(r"<a class=\"blue1\" href=\"(.*?)\" target=\"_blank\">(.*?)</a>", re.S)
            goods_name = pattern.findall(str(goods_name))
            for item in goods_name:
                goods_name = str(item[1])
                goods_url = "http://www.baowu.com" + str(item[0])

            # 商品大区
            area = table.find('dt').find_all('a')
            area1 = str(area[1].contents)
            area2 = str(area[2].contents)
            area3 = str(area[3].contents)

            # 过滤金币
            if '货在宝物网' in goods_name.replace("\n", ""):
                unit_price = 0
                pattern = re.compile(r"(.*?)刀币", re.S)
                game_currency = str(pattern.findall(goods_name)[0])

                if '亿刀币' in goods_name.replace("\n", ""):
                    hundred_million = game_currency.replace("亿","")
                    unit_price = Decimal(goods_price) / Decimal(hundred_million) / 10000

                if '万刀币' in goods_name.replace("\n", ""):
                    ten_thousand = game_currency.replace("万","")
                    unit_price = Decimal(goods_price) / Decimal(ten_thousand)

                if unit_price < 0.02 and unit_price > 0.001:
                    print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
                    print("单价：" + str(unit_price) + "元/万刀币")
                    print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')

                    print(goods_price.replace("\n", ""))
                    print(goods_name.replace("\n", ""))
                    print("游戏/区/服:" + area1 + "/" + area2 + "/" + area3)
                    print(goods_url + "\n")

            # 过滤王者套
            if '王者套' in str(goods_name).replace("\n", ""):

                if Decimal(goods_price) < 300:
                    print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
                    print("超值王者套：" + str(goods_price) + "元")
                    print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')

                    print(goods_price.replace("\n", ""))
                    print(goods_name.replace("\n", ""))
                    print("游戏/区/服:" + area1 + "/" + area2 + "/" + area3)
                    print(goods_url + "\n")


# 输出商品页码
def print_goods_info(url):
    global page_num
    global page_max
    print('======================================================')
    print('==================== 欢迎使用本系统 =====================')
    print('====================当前 页码数 ：' + str(page_num) + ' ======================')
    print('====================总页 页码为 ：' + str(page_max) + ' =====================')
    print('====================目标 网址为 ：' + url + ' =====================')
    print('======================================================')


# 主函数
if __name__ == '__main__':
    global page_num
    global page_max

    goal_object_urls = [
        'http://www.baowu.com/list/index.shtml?gameId=1&title=46hix2eaqxs2lfy&sellingOrSelled=1&orderby=price_asc&pageSize=80&pageNo=',
        'http://www.baowu.com/list/index.shtml?gameId=1&sellingOrSelled=1&orderby=price_asc&pageSize=80&pageNo=',
        'http://www.baowu.com/list/index.shtml?gameId=1&goodsType=1&sellingOrSelled=1&orderby=price_asc&pageSize=80&pageNo=',
        ]

    print('系统运行开始')
    t1 = time()

    for url in goal_object_urls:

        # 初始页码
        page_num = 1
        page_max = 10

        # 获取请求的URL地址
        request_url = url

        while (page_num < page_max):

            # 获取请求URL页面源码
            html_code = load_page(request_url + str(page_num))
            soup = BeautifulSoup(html_code, 'lxml')

            # 总页数
            record = soup.find('div', align="right")
            page_max = Decimal(str(record.findAll('span',class_='orange')[1].contents[0]))

            # # 输出信息
            # print_goods_info(request_url + str(page_num))

            # 商品信息列表
            goods_list = soup.find('div', class_='slistc0')
            tables = goods_list.find_all('dl')

            # 获取单个商品信息
            get_goods_info(tables)

            if len(tables) < 80:
                page_num = page_max

            page_num += 1

    t2 = time()
    print('本次消耗时间： ' + str(t2 - t1))