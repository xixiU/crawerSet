#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-27 17:56:46
# @Author  : yuan
# @Version : 1.0.0
# @describe: 爬虫主模块
import os,time
import string
from urllib import request
from urllib.parse import quote
import ssl
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from config import max_page, parse_result, debug_mode,singleton_timeout
from detail import Crawer
import csv
import socket
#设置所有单利演示
socket.setdefaulttimeout(singleton_timeout)
#打开csv
f_w  = open('%s.csv'%''.join(parse_result),'a',encoding='utf-8') 
fw_csv = csv.writer(f_w)
fw_csv.writerow(['title','url','pageCachePrefixName','QQ','Email'])

# 伪装浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}
# Cookie有点重要，不然访问要失败，不过也可以用selenium，省去了自己拼装的麻烦
bd_headers = {
    'Cookie': 'BIDUPSID=8640A1C37FE0690CCFD0ADC95CDD0614; PSTM=1573012288; BAIDUID=8640A1C37FE0690C2FF67C0B307E1236:FG=1; BD_UPN=12314753; BDSFRCVID=cHFOJeC62xSAeNnwFmf5T97SHxCLPfRTH6aVosjQ3KdSxvaQuPVtEG0Pjx8g0KA-Nb29ogKKXgOTHw0F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR-tVCtatCI3HnRv5t8_5-LH-UoX-I62aKDs-Dt2BhcqEIL4hhLV3-4X5pjrWlcPMDnU5R5ctfJ8DUbSj4Qo5Pky-H3pQROhfnAJKRQH0q5nhMJN3j7JDMP0-xPfa5Oy523ihn3vQpnbhhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0Djb-jN0qJ6FsKKJ03bk8KRREJt5kq4bohjnDjgc9BtQmJJrt2-T_5CQbflRmypo0bh-FBn8HJq4tQg-q3R7JJDTxEDO4jJQiWlTLQf5v0x-jLgbPVn0MW-5DSlI4qtnJyUPRbPnnBn-j3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFhJKIbhKLlejRjh-FSMgTK2Pc8bC_X3b7EfMjpsh7_bf--D6cLbpAe5JbqBTnK-4ceQhj1oMFGLpOxy5K_hP6x2U70WNOfLMcHbRclHDbHQT3mMRvbbN3i34jpWRuLWb3cWMnJ8UbS5T3PBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKJJ6LqJJ4HV-35b5raeR5g5DTjhPrM2RQAWMT-0bFH_---ahQofPcFLtTxej-9yMcU55cUJGn7_JjOWCOds-J2hU5hLnLW2b37BxQxtNRd2CnjtpvhHRnRbP5obUPUWMJ9LUvftgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCthMI04ejt35n-Wqx5KhtvtK65tsJOOaCvjOhQOy4oTj6Db0PQ-Wt6f3Djh_x-XJMO1JhOs0-jC3MvB-Jjyb-TIt23bb-nKKxjhVMQmQft20-IbeMtjBM_LBDuHVR7jWhviep72ybt2QlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjH62btt_tJk8_CoP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1427_21089_18560_29568_29220_28702; delPer=0; BD_CK_SAM=1; PSINO=7; COOKIE_SESSION=11616_0_9_9_7_46_0_3_9_6_8_20_261159_0_34_0_1574317407_0_1574317373%7C9%23334846_17_1574055214%7C4; BD_HOME=0; H_PS_645EC=a2613mtU9Z3zzlE3Z%2BGp%2Bj49ILi6lAP%2Fqx95Q%2FkEvc3CO5Lp9KZCsfjQvzU',
    # 'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',

}
# 百度搜索页面
bd_search_url = 'https://www.baidu.com/s?ie=utf-8&wd={}&pn={}'
# chrome_options = None
def getReallink(keyword,max_page):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://www.baidu.com')
    #通过ID找网页的标签，找到搜索框的标签          
    seek_input =   driver.find_element_by_id("kw")     
    #设置搜索的内容          
    seek_input.send_keys(keyword)    
    #找到搜索文档按钮          
    seek_but = driver.find_element_by_id("su")     
    #并点击搜索 按钮          
    seek_but.click()    
    #并点击搜索 按钮          
    # ge_link(driver.find_element_by_css_selector('a'))        
    js = 'document.documentElement.scrollTop=10000'#拖动滚动条到底部
    time.sleep(1)
    driver.execute_script(js)
    time.sleep(1)
    line_list = driver.find_elements_by_xpath("//h3[@class='t']")
    #'''xpath提取特征'''
    for line in line_list:
        t = line.find_element_by_xpath("a")
        print(t.text,t.get_attribute('href'))
        print(get_url(t.get_attribute('href')))
    #发送第一页
    # executor.submit(bd_search, driver.current_url,keyword,0)
    total = 0     #页面数

    #往后翻页
    while total<max_page:
        try:
            total=total+1
            if total == 1 :
                result = driver.find_element_by_xpath("//a[@class='n']")
                text=result.get_attribute('text')
                if text.find('下一页')>=0 :
                    result.click()    
                    time.sleep(2)

                    # executor.submit(bd_search, driver.current_url,keyword,total)
                    driver.execute_script(js)
                    #print('第'+total+'页')
            else :
                #result = driver.find_element_by_xpath("//a[@class='n']")
                result = driver.find_element_by_link_text("下一页>")    
                result.click()    
                time.sleep(2)

                # executor.submit(bd_search, driver.current_url,keyword,total)

                driver.execute_script(js)
     
        except:
            print("到最后一页了")
            break    
    driver.quit()      
#或者加密的url真实的链接
def get_url(url_path, head=bd_headers):
    if 'www' in url_path and url_path.startswith('www'):
        return url_path
    if 'baidu.com' not in url_path:
        print('在吧', url_path)
        return url_path
    if 'http' not in url_path:
        return None
    # 解決 'ascii' codec can't encode characters
    if False:
        s = quote(url_path, safe=string.printable)
        try:
            req = request.Request(s, None, head)
            with request.urlopen(req,timeout=singleton_timeout) as uf:
                return uf.geturl()
        except Exception as err:
            print('get_url', err)
        return None
    if True:
        s = quote(url_path, safe=string.printable)

        browser = webdriver.Chrome(chrome_options=chrome_options)
        try:
            browser.get(s)
            # 如果网页里面能find_elements_by_xpath找个元素的话,直接返回无需再等待
            # wait.until(lambda driver: browser.current_url)
            last_url = browser.current_url

            # 返回实际url
            return last_url
        except UnexpectedAlertPresentException:
            browser.switch_to.alert.accept()
        except Exception as err:
            print('@hl 启动浏览器获取url: ', url_path,err)
        finally:
            # 退出浏览器进程
            browser.quit()
    return None
# 爬取页面内容
def spider(url_path, head=headers, code='gbk'):
    data_html = ''
    # 解決 'ascii' codec can't encode characters
    s = quote(url_path, safe=string.printable)
    req = request.Request(s, None, head)
    try:
        with request.urlopen(req,timeout=singleton_timeout) as uf:
            while True:
                data_temp = uf.read(1024)
                if not data_temp:
                    break
                # 编码并返回字符串类型
                data_html += data_temp.decode(code, 'ignore')
    except Exception as err:
        print('spider--', err)
    return data_html

# 解析获取区下的部门名称
def parse_text(html_data, rule):
    if not html_data:
        return None
    try:
        # 转换为html对象，以便进行path查找
        html_obj = etree.HTML(html_data)
        # 补全网页标签
        last_html_data = etree.tostring(html_obj)
        # 再次转换为html对象
        html_obj = etree.HTML(last_html_data)
        # 采集朝阳部门名称
        depart_names = html_obj.xpath(rule)
        keys = []
        for item in depart_names:
            if hasattr(item, 'xpath'):
                keys.append(item.xpath('string(.)').strip())
            elif hasattr(item, 'text'):
                keys.append(item.text)
            else:
                keys.append(item)
        if len(keys) < 1:
            return None
        return keys
    except Exception as err:
        print('parse_text--', err)
    return None

def bd_search(url,name,page_id):
    # search_url = []
    
    get_all_titles = '//h3[@class="t"]/a[1]'  # 获取所有的搜索结果
    # get_title = '//*[@id="1"]/h3/a'  # 搜索结果标题

    # 采用动态组合id的方式获取结果
    # get_href = '//div[@class="f13"]/a[1]/text()'  # 这是不带http/https的域名
    # get_link = '//div[@class="f13"]/a[1]/@href'  # 从百度搜索的这个是一个外链

    # 采用：可以组合下面这两种方式获取url(不是外链)
    get_by_id = '//*[@id="occupy_id"]/div[2]/a[1]'  # 这是一个通过id获取第几个搜索结果
    get_by_id_a = '//*[@id="occupy_id"]/div/div[2]/div[2]/a[1]'  # 这是一个通过id获取第几个搜索结果
    get_by_id_span = '//*[@id="occupy_id"]/div/div[2]/span[1]'  # 这是一个通过id获取第几个搜索结果
   

    _search_url  = bd_search_url.format(name,page_id)
    searchStr = spider(url, bd_headers, 'utf-8')
    
    # 获取所有标题
    keyValues = parse_text(searchStr, get_all_titles)
    # 获取标题对应的真实的链接    
    if keyValues:
        for index in range(len(keyValues)):
            if debug_mode:print('搜索列表标题: ', keyValues[index], end=' ')
            # 上面获得的整个是简写的，需要自己判断和拼接，采用和获取href的方式如何？
            # print(_search_url,searchStr)
            urlRst = parse_text(searchStr, get_by_id.replace('occupy_id', str(index + 1)) + '/@href')
            print(urlRst)
            print(url,name,page_id,urlRst)
            
            # print(_search_url,urlRst)
            if not urlRst:
                # TODO 目前id对上有问题
                # print('gggg', get_by_id_a.replace('occupy_id', str(index + 1)) + '/@href')
                urlRst = parse_text(searchStr, get_by_id_a.replace('occupy_id', str(index + 1)) + '/@href')
            if not urlRst:
                
                urlRst = parse_text(searchStr, get_by_id_span.replace('occupy_id', str(index + 1)) + '/text()')
            if urlRst:
                for gv_url in urlRst:

                    trip_str = gv_url.strip().replace(' ', '')
                    if debug_mode:print(trip_str, end='\n')
                    real_url = get_url(trip_str)
                    if real_url:
                       
                        #在此处写入csv
                        prefix_fileName = '{}_{}_{}'.format(name,page_id,index)
                        print(prefix_fileName)
                        detail_info = Crawer(real_url,prefix_fileName).start()
                        one_iitem = [keyValues[index],real_url,prefix_fileName,detail_info[0],detail_info[1]]
                        fw_csv.writerow(one_iitem)
                        # print(one_iitem)
                        # search_url_dic = {'id': index, 'name': keyValues[index], 'linker': gv_url, 'url': real_url}
                        # search_url.append(search_url_dic)
                    else:
                        print('\n', index, keyValues[index], '不是一个有效链接: ', gv_url, '\n')
       

    # return search_url


if __name__ == '__main__':
    # 线程池
    executor = ThreadPoolExecutor(max_workers=64)
    tasks = []

    # 添加ssl认证
    ssl._create_default_https_context = ssl._create_unverified_context

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
    #getReallink(parse_result[0],max_page)
    task = executor.submit(getReallink,parse_result[0],max_page)
    for index in range(len(parse_result)):
        task = executor.submit(getReallink,parse_result[index],max_page)
        tasks.append(task)

    for index in range(len(parse_result)):
        for page_id in range(max_page):
            # print(parse_result[index],page_id)
            task = executor.submit(bd_search, parse_result[index],page_id*10)
            tasks.append(task)
        # time.sleep(search_page_timeout)


   
    for future in as_completed(tasks):
        try:
            future.result()
        except Exception:
            print("线程处理超时")
    f_w.close()

    print('结束\n')
