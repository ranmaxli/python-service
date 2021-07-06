#Python - Version: 
~~~
3.6.8
~~~

#Run - Linux
~~~
python3 src/main.py --common_config=conf/python-service.conf --env=$ENV
~~~

#Run - Pycharm Config

~~~
## Script path:
E:\workspace\python\python-service\src\main.py

## Parameters:
--common_config=conf/python-service.conf --env=$ENV

## Environment variables:
PYTHONUNBUFFERED=1

## Woking directoty:
E:\workspace\python\python-service\
~~~

#URL
~~~
http://localhost:2333/hello
~~~

#Tools 
~~~
## add_handler
python add_handler.py -m get AHandler /A
~~~

#Function
~~~
## bbdc(不背单词) 自定义词汇 生成脚本
该软件主要将我们日常所需要的记忆的词汇转换成“不背单词”自定义词汇所需要的文件格式

### 使用说明
1、找到一篇喜欢的文章，把文章内容复制下来，粘贴到docx文件下，并放置项目word-dictionary文件夹下。
2、更改读取的 get_word 方法中的 file=docx.Document(" URL ") 的地址
3、运行程序后可以到word-txt取名称为最新的txt文本上传至 bbdc.cn 取得最新词汇表

### 项目结构说明
#### word-dictionary
    用于存放用户自己整理的word单词文档
#### word-txt
    系统分析后生成的单词字典表
#### everyday-vocabulary.txt
    常用的词汇，如果你想屏蔽一些已经会的词汇，直接添加在这个文件中即可，系统分析时会直接跳过
#### read-docx-words.py
    项目主函数入口

## jd
大数据爬虫

## baowu
畅游刀剑英雄商品购买优惠连接

## daojian
畅游刀剑英雄测试区老友回归活动统计

~~~
