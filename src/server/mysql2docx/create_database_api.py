#! /user/bin/env python
# -*- coding: utf-8 -*

# 名称：
# 时间：2021-7-9 17:45:15
# 作者：ranmaxli

# 如果遇到问题可以参考这2篇博客
# https://ranmaxli.blog.csdn.net/article/details/108334758
# https://ranmaxli.blog.csdn.net/article/details/118611719

from Mysql2docx import Mysql2docx

m=Mysql2docx()

m.do('localhost', 'root', 'root', 'test', 3306)