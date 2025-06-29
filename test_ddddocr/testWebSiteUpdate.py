import requests
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   testWebSiteUpdate.py
@Date    :   2025/06/29 19:50:10
@Author  :   yuan 
@Desc    :   从网页获取的链接

```javascript
function extractInfringingUrls() {
  // 1. 选取所有 class 为 infringing_url 的 <li> 元素
  const listItems = document.querySelectorAll('li.infringing_url');

  // 2. 创建一个空数组来存放提取到的链接
  const urls = [];

  // 3. 遍历每一个获取到的元素
  listItems.forEach(item => {
    // 4. 获取元素的纯文本内容
    const fullText = item.textContent; // 例如："www.alipanba.com - 1 URL"

    // 5. 使用 ' - ' 作为分隔符来分割字符串
    const parts = fullText.split(' - ');

    // 6. 获取分割后的第一部分，并使用 trim() 清除可能存在的前后空格
    if (parts.length > 0) {
      const url = parts[0].trim();
      urls.push(url);
    }
  });

  // 7. 返回包含所有链接的数组
  return urls;
}
```
'''
import re
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse as parse_date
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

# --- 配置 ---
# 设置请求头，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# 设置请求超时时间（秒）
TIMEOUT = 10

def get_most_recent_from_sitemap(sitemap_url):
    """从站点地图URL中解析并返回最新的日期"""
    try:
        response = requests.get(sitemap_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        
        # 解析XML
        # 移除命名空间以便于查找标签
        xml_content = re.sub(' xmlns="[^"]+"', '', response.text, count=1)
        root = ET.fromstring(xml_content)
        
        latest_date = None
        
        # 查找所有 lastmod 标签
        for lastmod in root.findall('.//lastmod'):
            if lastmod.text:
                current_date = parse_date(lastmod.text)
                if latest_date is None or current_date > latest_date:
                    latest_date = current_date
        
        return latest_date
    except Exception as e:
        # print(f"  [Sitemap Error] {sitemap_url}: {e}")
        return None


def get_last_modified_date(url):
    """
    通过多种方法获取单个URL的最后修改日期
    方法顺序: 1. HTTP Header -> 2. Sitemap -> 3. HTML Meta Tags
    """
    try:
        # --- 方法一: 检查 HTTP Last-Modified Header ---
        response = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if 'Last-Modified' in response.headers:
            last_modified_str = response.headers['Last-Modified']
            return parse_date(last_modified_str)

        # --- 方法二: 检查并解析 Sitemap.xml ---
        # 尝试常见的sitemap路径
        sitemap_paths = ['/sitemap.xml', '/sitemap_index.xml']
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        for path in sitemap_paths:
            sitemap_url = urljoin(base_url, path)
            sitemap_date = get_most_recent_from_sitemap(sitemap_url)
            if sitemap_date:
                return sitemap_date

        # --- 方法三: 抓取HTML页面内容 ---
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # 寻找常见的元标签或时间标签
        # 规则可以根据目标网站的特征不断扩充
        meta_selectors = [
            'meta[property="article:modified_time"]',
            'meta[property="og:updated_time"]',
            'meta[name="last-modified"]',
            'meta[name="date"]',
        ]
        for selector in meta_selectors:
            tag = soup.select_one(selector)
            if tag and tag.get('content'):
                return parse_date(tag.get('content'))

        # 寻找 <time> 标签
        time_tag = soup.select_one('time[datetime]')
        if time_tag and time_tag.get('datetime'):
             return parse_date(time_tag.get('datetime'))

    except requests.exceptions.RequestException as e:
        # print(f"  [Request Error] {url}: {e}")
        return None
    except Exception as e:
        # print(f"  [General Error] {url}: {e}")
        return None
        
    return None # 如果所有方法都失败

# --- 主程序 ---
if __name__ == "__main__":
    
    # +---------------------------------------------------+
    # |                                                   |
    # |   请在这里粘贴您的网站清单 (一行一个网址)             |
    # |                                                   |
    # +---------------------------------------------------+
    websites_to_check = [
    "www.alipanba.com",
    "shikey.com",
    "www.666xit.com",
    "www.xuebapan.com",
    "www.dnflee.com",
    "52fz8.com",
    "www.ekcn.net",
    "pansou.cc",
    "www.dmzshequ.com",
    "www.aliyue.net",
    "shikey.com",
    "learn.lianglianglee.com",
    "www.ukoou.com",
    "wpfx.org",
    "it4clover.com",
    "www.5588.in",
    "juejin.cn",
    "m.douban.com",
    "baikeu.com",
    "lexuecode.com",
    "www.hyouit.com",
    "www.vipc6.com",
    "www.feimaoke.com",
    "www.sisuoit.com",
    "www.lqve888.com",
    "www.52xxzy.com",
    "cloud.tencent.com",
    "www.666xit.com",
    "www.fjha.net",
    "www.zx-cc.net",
    "qiuzhuti.com",
    "www.52pojie.cn",
    "www.javaxxz.com",
    "www.itxbzxw.com",
    "quan520.com",
    "kbzyz.com",
    "xkvbt.com",
    "zy.98ke.com",
    "www.javazx.com",
    "www.kebaiwan.com",
    "xiyou.pro",
    "www.cowcowit.com",
    "www.xuebapan.com",
    "www.ahhhhfs.com",
    "m.youxuan68.com",
    "shop.techins.xyz",
    "shikey.com",
    "shikey.com",
    "shikey.com",
    "www.java1234.com",
    "52fz8.com",
    "www.javaxxz.com",
    "www.dnflee.com",
    "www.ruike1.com",
    "shikey.com",
    "www.rurucode.com",
    "www.youxuan68.com",
    "freegeektime.com",
    "www.itxbzxw.com",
    "www.zx-cc.net",
    "www.jinreo.com",
    "www.java1234.com",
    "juejin.cn",
    "www.rh86.com"
]

    print(f"开始检查 {len(websites_to_check)} 个网站，请稍候...")
    
    results = []
    for site in websites_to_check:
        print(f"正在处理: {site}")
        last_update = get_last_modified_date(site)
        results.append({
            "site": site,
            "last_update": last_update
        })

    # 过滤掉没有找到更新日期的结果
    valid_results = [res for res in results if res['last_update']]

    # 按最近更新时间倒序排序
    # tzinfo is ignored for comparison, so we make them naive
    sorted_results = sorted(
        valid_results, 
        key=lambda x: x['last_update'].replace(tzinfo=None), 
        reverse=True
    )

    print("\n--- 检查完成 ---")
    print("最近更新时间排序结果 (倒序):\n")

    if not sorted_results:
        print("未能从任何网站获取到有效的更新日期。")
    else:
        for result in sorted_results:
            # 格式化日期显示
            formatted_date = result['last_update'].strftime('%Y-%m-%d %H:%M:%S %Z')
            print(f"网站: {result['site']}\n更新时间: {formatted_date}\n")