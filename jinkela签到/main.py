#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-28 19:37:59
# @Author  : x
# @Version : 1.0.0
# @describe: version 2 主爬取模块
import os,time


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import  singleton_timeout,debug_mode,main_site,id_password_set,proxy

import socket

#设置所有单例延时
socket.setdefaulttimeout(singleton_timeout)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

executable_path = '/usr/local/bin/chromedriver'
service = Service(executable_path)
def start(name_id:str,password:str):
    # print("chrome_options:%s"%chrome_options._arguments)
    try:
        print("chrome_options:%s"%options._arguments)

        driver = uc.Chrome(driver_executable_path= executable_path,options=options)

        # driver = webdriver.Chrome(service = service,options=chrome_options)

        driver.implicitly_wait(singleton_timeout)
        driver.get(main_site)
        # driver.maximize_window()

        driver.execute_script(f"window.open('{main_site}', '_blank')")
        time.sleep(7)
        driver.switch_to.window(driver.window_handles[1])
        seek_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
        # seek_name = driver.find_element_by_xpath("//input[@placeholder='账号']")
        seek_name.send_keys(name_id)    

        seek_mima = driver.find_element(By.XPATH,"//input[@id='passwd']")
        seek_mima.send_keys(password)
        #通过ID找网页的标签，找到搜索框的标签          
        # seek_input =   driver.find_element_by_id("kw")     
        #设置搜索的内容          
        #找到搜索文档按钮          
        seek_but = driver.find_element(By.XPATH,"//button[@id='login']")     
        #并点击搜索 按钮          
        seek_but.click()  
        print('login successful')
        # 找到签到按钮
        seek_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@id='checkin']")))
        seek_btn.click()
        print('checkin successful')
    except Exception as err:
        print(err)
    finally:
        # driver.quit()
        pass

def try_bypass_cloudfare(driver):
    try:
        # 等待确认元素出现
        checkbox = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cb-c input[type='checkbox']"))
        )
        # 点击复选框
        checkbox.click()
    except Exception as err:
        print(err) 

if __name__ == '__main__':
    # 线程池
    executor = ThreadPoolExecutor(max_workers=64)
    tasks = []

    # 启动参数 for selenium
    chrome_options = Options()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # 禁用图片的加载
            # 'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
        }
    }
    chrome_options.add_argument(f'user-agent={user_agent}')

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 启动参数 for undetected_chromedriver

    options = uc.ChromeOptions()

    # 设置代理
    options.add_argument(f"--proxy-server={proxy}")
    options.add_argument('—-ignore-certificate-errors')
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--auto-open-devtools-for-tabs")

    # chrome_options.add_argument('blink-settings=imagesEnabled=false')
    if len(proxy)>0:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    if not debug_mode:
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        # options.add_argument('--headless')
    # chrome 升级到129有bug，之后无头模式运行会报错https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/2030



    for id_pd in id_password_set:
        start(id_pd[0],id_pd[1])
    
    executor.shutdown(wait=True)#等待所有线程完成并销毁资源

    print('结束\n')
