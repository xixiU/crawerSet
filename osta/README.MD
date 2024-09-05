简介:国家资格证书查询定时任务<br>
说明：
1.依赖项<br>
```cmd
python3 -m pip install opencv-python
```

2.配置姓名、身份证号<br>
```cmd
# 三个参数任意配置2个
# 姓名
export MY_NAME=""

# 身份证号
export MY_CARD_NO=""

# 证书编号
export OSTA_CERTIFICATE_NO = ""
```

3.配置自动查询<br>
```
0 10 * * * /usr/bin/python3 /Users/yuanrongjie/software/python_project/crawerSet/osta/osta.py
```