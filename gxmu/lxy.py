#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-02-10 17:37:59
# @Author  : x
# @Version : 1.0.0
# @describe: 广西医科大学理学院教师信息抓取

# 从https://lxb.guat.edu.cn/szdw/azc/jslm2.htm获取教师信息，其中教师信息在<div class="content_list">元素下，通过href属性获取教师信息页面，然后从教师信息页面中获取教师姓名、邮箱

import re
from common import save_to_excel,get_page_soup,headers
import requests
from bs4 import BeautifulSoup

department = '理学院'
url = 'https://lxb.guat.edu.cn/szdw/azc/qtlm.htm'

soup = get_page_soup(url)
teachers = soup.find('ul', class_='content_list').find_all('a')
for teacher in teachers:
    teacher_name = teacher.string.strip()
    teacher_url = 'https://lxb.guat.edu.cn' + teacher['href'].split('..')[-1]
    # print(teacher_url)
    tearcher_detail_response = requests.get(teacher_url, headers=headers)
    tearcher_detail_response.encoding = tearcher_detail_response.apparent_encoding  # 自动识别编码
    detail_soup = BeautifulSoup(tearcher_detail_response.text, 'lxml')
    # 找到类<META Name="description" Content="个人简介  陈超，男，大学物理教研室，毕业于广西师范大学物理科学与技术学院的理论物理专业，现在桂林航天工业学院理学院从事教学、实验中心管理工作，主要研究领域有螺旋波动力学的研究、纳米材料过滤性能研究。研究领域  螺旋波动力学的研究、纳米材料过滤性能研究教育背景  1999.09-2003.06，广西师范大学，本科，专业：物理学；  2007.09-2010.06，广西师范大学，硕士研究生，专业：理论物理；工作经历    2010年7月至今在..." />的字符串，然后提取出邮箱
    # print(detail_soup.text)
    email = ''
    for p in detail_soup.find_all('p'):
        match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', p.get_text())
        if match:
            email =  match.group(0)
            break
    if email == '':
        continue

    save_to_excel(department,teacher_name, email)
    print("姓名：{},邮箱：{}".format(teacher_name,email))