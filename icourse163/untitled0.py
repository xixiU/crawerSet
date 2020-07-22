#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 18:53:20 2018

@author: xi
"""
import jieba
import os
import re

def process_line(line):
    try:
        line = line.replace('\n', '').replace('\u3000', '').replace('\u00A0', '')
        line = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=.\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]"," ", line)#去掉数字 以及其他字符
        line = ''.join(re.compile('[\u4e00-\u9fa5]',re.S).findall(line))#只保留汉字部分
        
        return line
    except UnicodeDecodeError:            
        return line
        
def compute_tf_by_file(filenames,output_filename  = 'data/text_seg.txt'):
    """
    for each file, calcute term frequency
    return format is :
        'word', 'file_name', term-frequency
    """
    
    word_docid_tf = []
    if not os.path.exists(os.path.dirname(output_filename)):
        os.mkdir(os.path.dirname(output_filename))
    output = open(output_filename, 'a', encoding='utf-8',)#训练数据和测试数据都需要写入
#    for name in filenames:
    with open(filenames, 'r', encoding="utf-8'") as f:
        tf_dict = dict()
        
        for line in f:
            line = process_line(line)
            words = jieba.cut(line.strip(), cut_all=False)
#                    words = pseg.cut(line.strip())
            #words = line.rstrip().split(separator)
            for word in words:
                output.write(word + ' ')
                tf_dict[word] = tf_dict.get(word, 0) + 1
            output.write('\n')#一行结束
    tf_list = tf_dict.items()
    word_docid_tf += [[item[0], filenames, item[1]] for item in tf_list]

#    return word_docid_tf   

if __name__=="__main__":
    compute_tf_by_file(filenames='268001.csv')