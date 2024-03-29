#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-28 19:37:59
# @Author  : x
# @Version : 1.0.0
# @describe: version 2 主爬取模块
import os,time
import string
import requests

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import  singleton_timeout,debug_mode,headers,id_password_set

import socket

#设置所有单利延时
socket.setdefaulttimeout(singleton_timeout)


def start(name_id,password):
    if(debug_mode):
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(chrome_options=chrome_options)

    #晨午检
    url = "https://xxcapp.xidian.edu.cn/site/ncov/dailyup"
    # url = 'https://xxcapp.某高校.edu.cn/ncov/wap/default/index'#疫情通
    # driver.maximize_window()
    driver.get(url)
    seek_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='账号']")))
    # seek_name = driver.find_element_by_xpath("//input[@placeholder='账号']")
    seek_name.send_keys(name_id)    

    seek_mima = driver.find_element_by_xpath("//input[@placeholder='密码']")
    seek_mima.send_keys(password)
    #通过ID找网页的标签，找到搜索框的标签          
    # seek_input =   driver.find_element_by_id("kw")     
    #设置搜索的内容          
    #找到搜索文档按钮          
    seek_but = driver.find_element_by_xpath("//div[@class='btn']")     
    #并点击搜索 按钮          
    seek_but.click()  
    
    time.sleep(3)
    #点击位置 
    #去掉只读
    # hidden = driver.find_element_by_xpath("//li[@style='display: none;']")
    # driver.execute_script("arguments[0].style.display = 'block';", hidden)
    driver.execute_script("""document.querySelector('input').removeAttribute("readonly")""")
    seek_location = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='点击获取地理位置']")))
    driver.execute_script("arguments[0].input.readonly = 'false';", seek_location)
    seek_location.click()

    time.sleep(2)
    #seek_btn=driver.findElement(By.cssSelector("a[href*='long']"))
    #找到提交按钮
    seek_btn= driver.find_element_by_xpath("//a/em[@class='tab-title-desc-little']")
    seek_btn.click()  
    #确认提交
    seek_confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='wapcf-btn wapcf-btn-ok']")))
    seek_confirm.click() 
    print(name_id,password,"successful")
    
    time.sleep(5)
            
 

if __name__ == '__main__':
    # 线程池
    executor = ThreadPoolExecutor(max_workers=64)
    tasks = []

    # 启动参数
    chrome_options = Options()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # 禁用图片的加载
            # 'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    for id_pd in id_password_set:
        start(id_pd[0],id_pd[1])
    
    executor.shutdown(wait=True)#等待所有线程完成并销毁资源

    print('结束\n')
