#! /user/bin/env python
# -*- coding: utf-8 -*

# 名称：检测老友回归活动
# 时间：2021-2-24 21:44:09
# 作者：李冉

# 老友回归大致时间范围：
# [219, 222, 224, 227, 228, 302,
# 520, 524, 527, 529, 601, 604, 606,
# 805, 820, 822, 823, 824, 901,
#  1028, 1031, 1102, 1111, 1122]

#  http://dj.changyou.com/


#导包
from time import time
import urllib.request
from bs4 import BeautifulSoup
import re


#全局变量
global page_num
global page_max
global index
global return_date_list


# 模拟IE9发送请求
def load_page(url):
    user_agent = 'Mozilla/5.0(compatible;MSIE 9.0;Windows NT 6.1;Trident/5.0;'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)
    resopnse = urllib.request.urlopen(req)
    html = resopnse.read()
    return html.decode()


# 获取商品的所有信息
def get_announce_test_info(tables):
    global page_num
    global page_max
    global index
    global return_date_list

    for table in tables:
        if table != '\n':
            link_url = table.find('a', target='_blank')
            pattern = re.compile(r"href=\"(.*?)\"", re.S)
            link_url = pattern.findall(str(link_url))
            for item in link_url:
                link_url = 'http://dj.changyou.com' + str(item)
                html_code = load_page(link_url)
                if '老友回归' in html_code:
                    pattern = re.compile(r"/test/(\d+)/", re.S)
                    retuen_date = pattern.findall(str(link_url))
                    for item in retuen_date:
                        retuen_date = str(item)
                    return_date_list.append(int(retuen_date[4:8]))
                    # print('☆☆☆☆☆☆☆☆☆ 老友回归开始咯 ☆☆☆☆☆☆☆☆☆☆')
                index += 1
                # print('第 ' + str(index) + ' 条测试服新闻 ' + link_url)




# 主函数
if __name__ == '__main__':
    global page_num
    global page_max
    global index
    global return_date_list

    print('系统运行开始')
    t1 = time()

    # 初始页码
    page_num = 1
    page_max = 10
    index = 0
    return_date_list = []

    while (page_num <= page_max):

        url = ''

        # 获取请求URL页面源码
        if page_num == 1:
            url = 'http://dj.changyou.com/dj/announce/test/test.shtml'
            html_code = load_page(url)
            soup = BeautifulSoup(html_code, 'lxml')
            # 总页数
            record = soup.find('div', class_="djPage")
            pattern = re.compile(r'共\d+条记录 \d\/(\d+)页', re.S)
            page_max = pattern.findall(str(record))
            for item in page_max:
                page_max = int(item)
        else:
            url = 'http://dj.changyou.com/dj/announce/test/test_' + str(page_num) + '.shtml'
            html_code = load_page(url)
            soup = BeautifulSoup(html_code, 'lxml')

        # 商品信息列表
        announce_list = soup.findAll('ul', class_='news_list')
        get_announce_test_info(announce_list[0].contents)

        page_num += 1

    # 统计每年活动大致范围
    return_date_list.sort()
    print(return_date_list)

    t2 = time()
    print('本次消耗时间： ' + str(t2 - t1))