#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:
@Date     :2024/08/29 23:10:08
@Author      :xixi
@version      :1.0
@File    :   测试ddddocr.py
'''
import ddddocr

slide = ddddocr.DdddOcr(det=False, ocr=False)
    
with open('target.png', 'rb') as f:
    target_bytes = f.read()

with open('background.png', 'rb') as f:
    background_bytes = f.read()

res = slide.slide_match(target_bytes, background_bytes,simple_target=True)

print(res)
print(res)