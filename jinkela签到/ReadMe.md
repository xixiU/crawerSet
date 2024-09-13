## 作用

用来签到

## 使用

0. 下载chromedrive驱动
在[https://googlechromelabs.github.io/chrome-for-testing/#stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)下载对应的chrome版本镜像,并放在/usr/bin/（linux）或其他系统目录

1. 设置账号密码
在config.py设置自己的账号密码；

2. 运行
```python
python3 main.py
```

建议测试时将config.py中的debug_mode设置为Tue,测通后设置为False

## 类Unix使用crontab配置定时任务
通过crontab 配置自动运行。

编辑当前用户的 crontab
```cmd
crontab -e
```

添加如下内容
```cmd
* * */1 * * path_of_your_python path_of_file/main.py
```

配置每天运行