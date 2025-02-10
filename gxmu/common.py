import os
import pandas as pd
import openpyxl
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.487.0 Safari/537.36 Edg/100.0.1185.39'
    }

def get_page_soup(url:str):
    
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def save_to_excel(department:str,name:str, email: str):
    # **追加数据到 Excel**
    file_path = "data.xlsx"  # Excel 文件名

    # 检查 Excel 是否存在
    if not os.path.exists(file_path):
        # 如果文件不存在，创建一个新的 Excel 并写入表头
        df = pd.DataFrame(columns=["学校","学院","姓名", "邮箱"])
        df.to_excel(file_path, index=False, engine='openpyxl')

    # 读取 Excel 并追加数据
    df = pd.read_excel(file_path, engine='openpyxl')
    new_data = pd.DataFrame([["广西医科大学",department,name, email]], columns=["学校","学院","姓名", "邮箱"])
    df = pd.concat([df, new_data], ignore_index=True)

    # 保存回 Excel
    df.to_excel(file_path, index=False, engine='openpyxl')