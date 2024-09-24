#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   osta.py
@Date    :   2024/09/05 14:27:17
@Author  :   yuan 
@Desc    :   osta成绩查询
'''
import os
import requests
from dataclasses import dataclass, field
from typing import Optional
import json
import curlify
from detect_move import detect_horizontal_movement
COMMON_HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': '_gscu_486005091=22222899kg836m17; Hm_lvt_e85984af56dd04582a569a53719e397f=1724897304; _gscbrs_486005091=1; _gscs_486005091=255168193yebif46|pv:2',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://jndj.osta.org.cn/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
@dataclass
class BaseBody:
    slidingImage: str
    originalImage: str
    xWidth: Optional[int] = field(default=None)
    yHeight: int = field(default=0)
    uniqueId: str = field(default="")
    
@dataclass
class ApiResponse:
    code: int
    msg: str
    body: BaseBody


def from_dict(data_class, data_dict):
    """通用字典转换函数，将字典转换为数据类实例"""
    from collections.abc import Mapping

    def is_dataclass_instance(obj):
        return isinstance(obj, type) and hasattr(obj, "__dataclass_fields__")

    fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}

    return data_class(**{
        field_name: from_dict(fieldtypes[field_name], data_dict[field_name]) 
        if is_dataclass_instance(fieldtypes[field_name]) and isinstance(data_dict[field_name], Mapping)
        else data_dict[field_name]
        for field_name in data_dict
    })

def getBaseUnic() -> BaseBody:
    url = 'http://jndj.osta.org.cn/api/certificate/get/verification/base'

    response = requests.get(url, headers=COMMON_HEADERS, verify=False)
    assert response.status_code == 200  ,"base信息获取失败"+response.text
    repsone_text = response.text
        # 解析 JSON 字符串为字典
    parsed_dict = json.loads(repsone_text)

    # 将字典转换为数据类实例
    api_response = from_dict(ApiResponse, parsed_dict)

    return api_response.body

def getScore(param : BaseBody):
    url = "http://jndj.osta.org.cn/api/certificate/query/list/jn"
    params = {
        "code": param.uniqueId,
        "num": str(detect_horizontal_movement(param.originalImage,param.slidingImage)),
        "name": os.getenv("MY_NAME"),
        "cardNo":os.getenv("MY_CARD_NO"),
        "certificateNo":  ''
    }
    response = requests.get(url, headers=COMMON_HEADERS, params=params)
    # print(curlify.to_curl(response.request))
    return response.json()
 

def getScoreOnce():
    data = getScore(getBaseUnic())
    if data["code"]!=200:
        return getScoreOnce()
    print(data)
if __name__ == "__main__":
    getScoreOnce()