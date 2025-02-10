#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-02-10 19:37:59
# @Author  : x
# @Version : 1.0.0
# @describe: 广西医科大学医学院教师信息抓取

# 从https://yxy.gxmu.edu.cn/rcpy_2647/szdw/yxy_fqzjs/获取教师信息，其中教师信息在<div class="list-all">元素下，每一个<a target="_blank" href="./t198542.html" title="黄雪秋">通过href属性获取教师信息页面，然后从教师信息页面中获取教师姓名、邮箱
import requests
from bs4 import BeautifulSoup
import re
from common import save_to_excel,get_page_soup,headers

department = '医学院'
url = 'https://yxy.gxmu.edu.cn/rcpy_2647/szdw/yxy_xzzcdw/'

soup = get_page_soup(url)
teachers = soup.find('div', class_='list-all').find_all('a')
for teacher in teachers:
    teacher_name = teacher.string.strip()
    teacher_url = url + teacher['href']
    # print(teacher_url)
    tearcher_detail_response = requests.get(teacher_url, headers=headers)
    tearcher_detail_response.encoding = tearcher_detail_response.apparent_encoding  # 自动识别编码
    detail_soup = BeautifulSoup(tearcher_detail_response.text, 'lxml')
    # print(detail_soup)
    # 找到类似<span data-index="" style="line-height: 150%; font-size: 16px; font-family: 宋体, SimSun;">2.电子邮箱：113zhwall@163.com</span>的字符串，然后提取出邮箱
    email = ''
    for span in detail_soup.find_all('span'):
        match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', span.get_text())
        if match:
            email =  match.group(0)
            break
    if email == '':
        continue
    # 将结果追加写入到excel中
    # with open('teacher.txt','a',encoding='utf-8') as f:
    #     f.write("姓名：{},邮箱：{}\n".format(teacher_name,email))
    save_to_excel(department,teacher_name, email)
    print("姓名：{},邮箱：{}".format(teacher_name,email))
