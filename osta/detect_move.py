#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   detect_move.py
@Date    :   2024/09/05 17:53:40
@Author  :   rongjie.yuan 
@Desc    :   检测滑块移动
'''
import cv2
import numpy as np
import base64

def saveImage(source,fileName):

    # 解码Base64数据
    image_data = base64.b64decode(source)

    # 保存为文件
    with open(fileName, 'wb') as f:
        f.write(image_data)

    print("Image successfully saved as "+fileName)
    
# 解码base64图像
def decode_base64_to_image(base64_str):
    img_data = base64.b64decode(base64_str)
    image = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

def detect_horizontal_movement(sliding_image_base64,original_image_base64):

    sliding_image = decode_base64_to_image(sliding_image_base64)
    original_image = decode_base64_to_image(original_image_base64)

    # 使用模板匹配找出滑块在原始图像中的位置
    result = cv2.matchTemplate(original_image, sliding_image, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # 得到滑块的起始位置和模板匹配检测到的位置
    initial_position = 0  # 通常滑块起始位置为0或中间某点
    detected_position = max_loc[0]

    # 计算滑块的水平位移
    horizontal_movement = detected_position - initial_position

    return horizontal_movement