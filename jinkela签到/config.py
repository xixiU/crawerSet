#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:       :
@Date     :2022/11/02 22:15:53
@Author      :xia
@version      :1.0
'''
# chrome driver下载
# 海外https://chromedriver.chromium.org/downloads
# 国内镜像 https://registry.npmmirror.com/binary.html?path=chromedriver/

# 主站地方方便切换
main_site = 'https://jinkela.lol/auth/login'

#　debug模式会显示Ui,正常运行可以不启动ｕi，在非windowsX环境配置定时脚本　，可以自动填
debug_mode = True 
# 多线程调用每个现成延时
# time out for single page
singleton_timeout = 5
 #支持多线程调用，填上多人的信息即可
id_password_set=[("verjue@163.com","5nEj7.vds53VtXB")]


