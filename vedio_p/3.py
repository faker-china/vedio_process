# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 3.py
# @Time     : 2024/10/24 下午5:25
# @Software : PyCharm
import os
import re


def calculate_ratio(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式查找所有书名号内的内容
    matches = re.findall(r'“(.*?)”', content)

    # 计算书名号内文字的总数
    total_text_within_quotes = sum(len(match) for match in matches)

    # 计算整个文本的字符数
    total_characters = len(content)

    # 计算比值
    ratio = total_text_within_quotes / total_characters if total_characters > 0 else 0

    return ratio


def process_folder(folder_path):
    results = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                ratio = calculate_ratio(file_path)
                results[file_path] = ratio
    return results


# 替换为你的文件夹路径
folder_path = r'C:\Users\bilingbiling\Desktop\A\新建文件夹'
results = process_folder(folder_path)

# 打印结果
for file_path, ratio in results.items():
    print(f"{file_path}: {ratio:.2%}")

