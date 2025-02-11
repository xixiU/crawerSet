#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-02-10 17:37:59
# @Author  : x
# @Version : 1.0.0
# @describe: 桂林理工大学教师信息抓取

# 从https://faculty.glut.edu.cn/py_teacherlist.jsp?urltype=tsites.PinYinTeacherList&wbtreeid=1001&py=a&lang=zh_CN获取教师信息，其中教师信息在<div class="content_list">元素下，通过href属性获取教师信息页面，然后从教师信息页面中获取教师姓名、邮箱
import requests
from bs4 import BeautifulSoup
import re
from common import save_to_excel,get_page_soup,headers
import string

def decode_email(teacher_url:str,encrypted_content:str):
        # 发送请求
    payload = {
        "id": '_tsites_encryp_tsteacher_tsemail',
        "content": encrypted_content,
        "mode": "8"  # 这个值来自 `_tsites_com_view_mode_type_`，可能需要抓包确认
    }

    decode_headers = {
        "User-Agent": headers['User-Agent'],
        "Referer": teacher_url,  # 需要替换成实际网站
    }
    response = requests.get('https://faculty.glut.edu.cn/system/resource/tsites/tsitesencrypt.jsp', params=payload, headers=decode_headers)
    data = response.json()
    decrypted_email = data.get("content", "解密失败")
    return decrypted_email

def get_next_page_url(soup):
    """
    获取下一页的URL
    
    Args:
        soup: BeautifulSoup对象
    
    Returns:
        str: 下一页URL,如果没有下一页则返回None
    """
    # 查找带有class="Next"的a标签
    next_link = soup.find('a', class_='Next')
    
    if next_link:
        # 存在下一页,返回完整URL
        return 'https://faculty.glut.edu.cn/py_teacherlist.jsp' + next_link.get('href')
    
    # 不存在下一页,返回None
    return None

def get_teacher_info(url:str):
    soup = get_page_soup(url)
    teachers = soup.find('div', class_='rowbox teachbox').find_all('li')
    # 处理当前页
    for teacher in teachers:
        teacher_url = teacher.find('a')['href']
        namebox = teacher.find('div', class_='namebox') if teacher else None
        teacher_name = namebox.find('h1').get_text(strip=True) if namebox else None
        print(teacher_name,teacher_url)
        tearcher_detail_response = requests.get(teacher_url, headers=headers)
        tearcher_detail_response.encoding = tearcher_detail_response.apparent_encoding  # 自动识别编码
        detail_soup = BeautifulSoup(tearcher_detail_response.text, 'lxml')
        email = ''
        # 找到id为_tsites_encryp_tsteacher_tsemail的标签
        email_encode = detail_soup.find(id='_tsites_encryp_tsteacher_tsemail')
        if email_encode:
            # print(teacher_url,email_encode.text)
            email = decode_email(teacher_url,email_encode.text)
        # 找到 p标签下面的 xx学院，xx只能是中文,通过正则表达式查找,只需要找到一个即可
        department_reg_pattern = r'(物理与电子信息工程学院|地球科学学院|环境科学与工程学院|材料科学与工程学院|化学与生物工程学院|土木工程学院|测绘地理信息学院|计算机科学与工程学院|机械与控制工程学院|珠宝学院|马克思主义学院|（?:思想政治理论教学部）|公共管理与传媒学院|商学院|旅游与风景园林学院|艺术学院|外国语学院|数学与统计学院|南宁分校|继续教育学院|国际教育学院(?:国际交流处)、港澳台事务办公室|人文素质教育教学部|体育教学部)'
        match = re.search(department_reg_pattern, detail_soup.text)
        department = match.group(0) if match else '未知'
        if email == '':
            continue

        save_to_excel(department,teacher_name, email,school='桂林理工大学')
        print("姓名：{},邮箱：{},学院：{}".format(teacher_name,email,department))
    # 判断是否有下一页
    next_page_url = get_next_page_url(soup)
    if next_page_url:
        print("翻页处理下一页")
        get_teacher_info(url=next_page_url)
# 字母拼音,从a到z进行遍历
for py in string.ascii_lowercase:
    url = f'https://faculty.glut.edu.cn/py_teacherlist.jsp?urltype=tsites.PinYinTeacherList&wbtreeid=1001&py={py}&lang=zh_CN'
    get_teacher_info(url)
# 测试
#get_teacher_info('https://faculty.glut.edu.cn/py_teacherlist.jsp?urltype=tsites.PinYinTeacherList&wbtreeid=1001&py=l&lang=zh_CN')
