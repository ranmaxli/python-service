#! /user/bin/env python
# -*- coding: utf-8 -*

# 名称：宠物商城数据录入 京东商城关键字商品基本信息
# 时间：2019-2-16 22:40:47
# 作者：李冉

#  https://www.jd.com/

#导包
import urllib #基础爬虫包
import urllib.request
import re
import pymysql.cursors #数据连接包
import linecache #随机数包
import random
import datetime
import time

#全局变量
global price_state # 检查 是否获取到金额数据
global salesVolume_state # 检查 是否获取到商品销量
global keyWordNumber # 记录关键字遍历到第几个
global pageNumber # 记录页码数到第几页
global goodsNumber # 记录到第几个商品


# 模拟IE9发送请求
def load_page(url):
    user_agent = 'Mozilla/5.0(compatible;MSIE 9.0;Windows NT 6.1;Trident/5.0;'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)
    resopnse = urllib.request.urlopen(req)
    html = resopnse.read()
    return html

# 获取本地的关键字
def iget_localKeyword():
    # 本地的关键字地址文件
    f = open("keyword.txt", "r",encoding='UTF-8')
    # 逐行读取所有内容
    lines = f.readlines()
    #定义数组存放数据
    keyword=[]
    #遍历获取所有数据
    for line in lines:
        line=urllib.request.quote(line)
        keyword.append(line)
    #返回获取的所有数据
    return keyword

# 获取本地的商品发货地址
def get_localAddress():
    # 随机获取商品的发货地址
    for i in range(1, 2586):  # for循环几次
        a = random.randrange(1, 2586)  # 1-9中生成随机数
        sendAddress = linecache.getline(r'address.txt', a)
        return sendAddress

#获取商品的所有信息
def get_goodsInfo(url):

    #全局变量
    global keyWordNumber
    global pageNumber
    global goodsNumber
    global salesVolume_state
    global price_state

    #局部变量
    goods_store=""
    goods_herf=""
    goods_url=""
    goods_name=""
    goods_price=""

    try:

        # 获取当前搜索内容
        pattern = re.compile(r"window.QUERY_KEYWORD='(.*?)';", re.S)
        search_content = pattern.findall(url)
        for item in search_content:
            search_name = item.replace("'", "").replace("﻿","")

        #获取一个商品模块的 DIV
        pattern = re.compile(r"class=\"gl-item\"([\s\S]*?)<\/a><\/span>		<\/div>", re.S)
        DIV_content = pattern.findall(url)
        # 获取不到商品数据 进行第二次匹配
        if len(DIV_content)==0:
            # print("获取不到商品数据 进行第二次匹配")
            pattern = re.compile(r"class=\"gl-item\"([\s\S]*?)加入购物车", re.S)
            DIV_content = pattern.findall(url)
        DIV_index = 0
        for item in DIV_content:
            DIV_txt = item
            DIV_index +=1
            sendAddress = get_localAddress()# 获取随机地址
            print ("goodsNumber:" + str(goodsNumber+1) +" , "+ "keyword:" + search_name +" , "+"page:"+str(pageNumber)+" , "+"module:"+ str(DIV_index)+" , "+"sendAddress:"+sendAddress)

            # 店铺名称
            pattern = re.compile(r"html\" title=\"(.*?)\">", re.S)
            store_content = pattern.findall(DIV_txt)
            for item in store_content:
                goods_store = item.replace("京东", "").replace("【京东超市】", "").replace(",", "")
                print ("店铺名称："+goods_store)
                break

            # 商品地址
            pattern = re.compile(r"data-pid=\"(.*?)\"", re.S)
            herf_content = pattern.findall(DIV_txt)
            if(len(herf_content)!=0):
                herf_index = 0
                herf_list = []
                herf_list.append(str(herf_content[herf_index]))
                goods_herf = herf_list[herf_index] +".html"
                print("商品地址:" + "item.jd.com/" + goods_herf)
            if (len(herf_content) == 0):
                try:
                    pattern = re.compile(r"pid=(\d+)&", re.S)
                    herf_content = pattern.findall(DIV_txt)
                    herf_index = 0
                    herf_list = []
                    herf_list.append(str(herf_content[herf_index]))
                    goods_herf = herf_list[herf_index] + ".html"
                    print("商品地址:" + "item.jd.com/" + goods_herf)
                except:
                    print("Error: list index out of range")

            # 商品图片 (默认选第一个，解决京东代码优化有出现多条数据)
            pattern = re.compile(
                r"<img width=\"220\" height=\"220\" class=\"err-product\" data-img=\"1\" (.*?)=\"(.*?)\" />", re.S)
            picture_content = pattern.findall(DIV_txt)
            picture_index = 0
            picture_list = []
            while (picture_index < len(picture_content)):
                picture_list.append("http:" + str(picture_content[picture_index][1]))
                goods_url = picture_list[picture_index]
                print("商品图片:"+goods_url)
                picture_index += 1
                break

            # 商品名称 (默认选第一个，解决京东代码优化有出现多条数据)
            pattern = re.compile(r"<div class=\"p-name p-name-type-2\">\s*<a\s*target=\"_blank\" title=\"([^'\"]*)\"", re.S)
            title_content = pattern.findall(DIV_txt)
            for item in title_content:
                goods_name = item.replace("京东", "").replace("【京东超市】","").replace(",","")
                print ("商品名称:"+goods_name)
                break


            # 商品价格 (默认选第一个，解决京东代码优化有出现多条数据)
            price_state = "error"
            pattern = re.compile(r"<em>￥</em><i>(.*?)</i></strong>", re.S)
            price_content = pattern.findall(DIV_txt)
            # 捕获异常 解决：商城前端代码维护后，程序运行异常问题 could not convert string to float
            try:
                for item in price_content:
                    goods_price = float(item)
                    print("商品价格:" + str(goods_price))
                    price_state = "true"
                    break
            except:
                print ("Error: could not convert string to float")

            if price_state =="error":
                #无相关数据进行跨域查找
                pattern = re.compile(r"<strong class=\"(.*?)\"></strong>", re.S)
                price_class = pattern.findall(DIV_txt)
                for item in price_class:
                    price_find = str(item)
                    break
                #二次寻找后 部分数据异常 这里不再做处理
                pattern = re.compile(r"<strong class=\"%s\" data-adv=\"1\"><em>￥</em><i>(.*?)</i></strong>" % (price_find), re.S)
                price_find=pattern.findall(url)
                for item in price_find:
                    price_sum = str(item)
                    goods_price = float(price_sum)
                    print ("商品价格:"+ str(goods_price))
                    break
                print ("--提示：此模块为异常数据，若三次查询无果，请您随机赋值 【商品价格】--")


            #商品销量
            salesVolume_state=""
            pattern = re.compile(r"\'flagsClk=(.*?)\">(.*?)<", re.S)
            salesVolume_content = pattern.findall(DIV_txt)
            salesVolume_list = list(salesVolume_content)
            salesVolume_str = str(salesVolume_list)
            #第一次尝试获取
            salesVolume_state = salesVolume_str[81:-1].replace("'","").replace(")","").replace(" ","").replace("+","")
            #正则判断获取的数据是否含有非法字符
            pattern = re.compile(r",", re.S)
            salesVolume_stateRE = pattern.findall(salesVolume_state)
            salesVolume_stateREContent=""#获取正则后的内容 判断是否满足条件输出
            for item in salesVolume_stateRE:
                salesVolume_stateREContent = item
                break
            if(salesVolume_stateREContent==","):
                # 第二次尝试获取
                salesVolume_state=salesVolume_str[95:104].replace("\'","").replace(")","").replace(",","").replace("(","").replace("\"","").replace(" ","").replace("+","")
                goods_salesValue = salesVolume_state
                print ("商品销量:"+str(goods_salesValue) + "\n")
                if (salesVolume_stateREContent==""):
                    print ("--提示：此模块为异常数据，若三次查询无果，请您随机赋值 【商品销量】--")
            else:
                goods_salesValue = salesVolume_state
                print("商品销量:" + str(goods_salesValue) + "\n")

            # 处理异常
            if (goods_name == ''):  # 爬取数据为空异常
                break
            if (goods_url == ''):  # 商品地址异常
                break
            if (goods_store == ''):  # 商店名称异常
                goods_store = '旗舰店'
            if (str(goods_price) == ''):  # 商品价格异常
                goods_price = random.randrange(0, 1000)
            if (str(goods_salesValue) == '' or str(goods_salesValue) == ']'):  # 商品销售量异常
                goods_salesValue = random.randrange(0, 1000)
            goods_herf = "item.jd.com/" + goods_herf;  # 商品地址异常

            # 定位问题
            if goods_herf.find("item.jd.com/item.jd.com/") != -1:
                print("Error:获取商品地址失败");
            if goods_herf == "item.jd.com/":
                print("Error:获取商品地址失败");

            # 累加商品数量
            goodsNumber += 1

            # 连接数据库
            connect = pymysql.Connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='root',
                db='petshop',
                charset='utf8'
            )

            # 获取游标
            cursor = connect.cursor()

            # 插入数据
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
            sql = "insert into petshop_goodsbrief values ('" + goods_herf + "','" + str(goods_name) + "','" + str(goods_price) + "','" + str(goods_salesValue) + "','"+goods_store+"','" + str(sendAddress) + "','" + str(goods_url)  + "','" + str(nowTime)  + "','" + str(search_name) + "')"
            # sql = "insert into petshop_goodsbrief values ('" + goods_herf + "','" + str(goods_name) + "','" + str(goods_price) + "','" + str(goods_salesValue) + "','"+goods_store+"','" + str(sendAddress) + "','" + str(goods_url)  + "','" + str(nowTime) + "')"
            cursor.execute(sql)
            connect.commit()

            # 关闭连接
            cursor.close()
            connect.close()

    except:
        print("Error: 当前商品的页面数据为空或已存在数据库，自动进入当前商品关键字的下一页进行检索")

#主函数
if __name__ == '__main__':

    keyWordNumber = 0
    pageNumber = 1
    goodsNumber = 0
    sleepTime = 5

    # 获取关键字内容
    while (keyWordNumber < len(iget_localKeyword())):
        # 获取商品关键字
        keyword = iget_localKeyword()[keyWordNumber]
        # 获取不同页码下的商品信息
        while (pageNumber <= 100):
            # 获取请求的URL地址
            request_url = ("https://search.jd.com/Search?keyword=" + keyword + "&wq=" + keyword + "&page=" + str(pageNumber) + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&click=0")
            # 获取请求URL页面源码
            url_code = load_page(request_url).decode('utf-8')
            # 过滤京东没有的商品信息
            state = 'error'
            pattern = re.compile(r"抱歉，没有找到与“<em>﻿(.*?)</em>”相关的商品", re.S)
            content = pattern.findall(url_code)
            for item in content:
                print("抱歉，没有找到与“" + item + "”相关的商品")
                state = 'true'
                break
            if state == 'error':
                # 获取下载商品信息
                get_goodsInfo(url_code)
                # 继续获取下一页商品内容
                pageNumber += 1
            else:
                pageNumber = 101
            # 防爬虫 sleep
            if pageNumber % 10 == 0:
                time.sleep(sleepTime)
        # 继续操作下一个关键字内容
        keyWordNumber += 1
        # 重置页面数
        pageNumber = 1
        # 防爬虫 sleep
        time.sleep(sleepTime*6)