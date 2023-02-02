## 作用

用来签到

## 使用

0. 在[http://npm.taobao.org/mirrors/chromedriver/](http://npm.taobao.org/mirrors/chromedriver/)下载对应的chrome版本镜像

1.在config.py设置自己的账号密码；

2.
```python
python3 main.py
```

建议测试时将config.py中的debug_mode设置为Tue,测通后设置为False

## 类Unix使用crontab配置定时任务

1.crontab -e
2.* * */1 * * path_of_your_python path_of_file/main.py

配置每天运行