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
def wait_for_human_verification(driver, timeout=30):
    """
    尝试自动点击 Turnstile checkbox；如果自动点击无效，保存截图并等待用户手动通过（在可见浏览器中）。
    返回 True 表示验证通过（页面出现 input#email 或 success UI），否则 False。
    """
    import time
    from selenium.common.exceptions import (
        ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
    )

    # 1) 尝试自动点击 cf 复选框（如果可点击）
    try:
        checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cb-c input[type='checkbox']"))
        )
        try:
            checkbox.click()
            # 等待可能的验证过程（verifying -> success）
            end = time.time() + timeout
            while time.time() < end:
                # 若页面出现邮箱输入框，说明验证通过
                if driver.execute_script("return document.querySelector('input#email') !== null && document.querySelector('input#email').offsetParent !== null"):
                    return True
                # 或者检测 success 区块显示
                success_visible = driver.execute_script("""
                    const s = document.getElementById('success');
                    return s && (s.style.display !== 'none' && s.offsetParent !== null);
                """)
                if success_visible:
                    return True
                time.sleep(0.5)
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            # 自动点击失败，继续到人工流程
            print("自动点击 Cloudflare 复选框失败：", e)
    except Exception:
        # 未找到可点击的 checkbox（可能 Turnstile 非标准嵌套），后续走人工流程
        pass

    # 2) 自动点击不生效 -> 保存截图并提示人工操作
    try:
        ts = int(time.time())
        screenshot_path = f"/tmp/cf-{ts}.png"
        driver.save_screenshot(screenshot_path)
        with open(f"/tmp/cf-{ts}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Cloudflare 验证需要人工处理。页面截图已保存到: {screenshot_path}")
        print("请在浏览器中手动完成“确认您是真人”的验证，然后回到终端按回车继续。")
    except Exception as e:
        print("保存页面快照失败：", e)
        print("请在浏览器手动通过 Cloudflare，然后回车继续。")

    # 如果脚本在 headless 模式运行，人工操作不可行 -> 提示并返回 False
    try:
        if "--headless" in " ".join(driver.capabilities.get("goog:chromeOptions", {}).get("args", []) or []):
            print("注意：当前为 headless 模式，无法进行人工点击。请在有头模式下运行脚本或移除 --headless 参数。")
    except Exception:
        pass

    # 阻塞等待用户回车（手动完成验证后继续）
    try:
        input("完成 Cloudflare 验证后按回车继续 ...")
    except Exception:
        # 在某些环境下 input 可能不可用，改为等待固定时间
        print("无法等待键盘输入，改为等待 30s 后继续。")
        time.sleep(30)

    # 验证是否真的通过（检测邮箱输入框或 success UI）
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#email"))
        )
        return True
    except Exception:
        # 最后一次检查 success 区块
        success_visible = driver.execute_script("""
            const s = document.getElementById('success');
            return s && (s.style.display !== 'none' && s.offsetParent !== null);
        """)
        return bool(success_visible)

def start(name_id: str, password: str):
    try:
        print("chrome_options:%s" % options._arguments)

        # 建议让 uc 管理驱动，或确保 executable_path 正确。这里仍沿用你的调用方式：
        driver = uc.Chrome(driver_executable_path=executable_path, options=options)
        
        # driver = webdriver.Chrome(service = service,options=chrome_options)
        driver.implicitly_wait(singleton_timeout)

        # 打开页面（建议不要立即新开 tab，先在当前 tab 处理验证）
        driver.get(main_site)
        time.sleep(1)
        # 如果你确实需要新开 tab，可以在通过验证后再打开
        # driver.execute_script(f"window.open('{main_site}', '_blank')")

        # 先处理 Cloudflare 验证（如果存在）
        try:
            # 先快速检测页面中是否存在 Turnstile / Cloudflare 验证区
            cf_exists = driver.execute_script("return !!document.querySelector('div.cb-c') || !!document.getElementById('uMtSJ0');")
            if cf_exists:
                print("检测到 Cloudflare 验证，开始处理...")
                ok = wait_for_human_verification(driver, timeout=30)
                if not ok:
                    print("Cloudflare 验证仍未通过，抛出异常或跳过此账号。")
                    raise RuntimeError("Cloudflare verification failed or not completed")
                print("Cloudflare 验证通过，继续登录流程。")
        except Exception as e:
            print("处理 Cloudflare 验证时出错：", e)
            raise

        # 页面验证通过后，切换/刷新以确保输入框可用
        time.sleep(1)
        driver.refresh()
        # 等待邮箱输入框可见
        seek_name = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#email"))
        )
        # seek_name = driver.find_element(By.ID,"email")
        seek_name.send_keys(name_id)

        seek_mima = driver.find_element(By.CSS_SELECTOR, "input#password")
        seek_mima.send_keys(password)

        seek_but = driver.find_element(By.CSS_SELECTOR, "button#login_submit")
        seek_but.click()
        print('login successful')

        # 找到签到按钮
        seek_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#checkin"))
        )
        seek_btn.click()
        print('checkin successful')

    except Exception as err:
        print("start() exception:", err)

    finally:
        # driver.quit()
        pass


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
