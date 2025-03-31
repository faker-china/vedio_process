# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 统计文件名称.py
# @Time     : 2024/8/13 上午11:05
# @Software : PyCharm
import os
import pandas as pd


def list_files_recursively(startpath):
    """
    递归地列出指定路径下所有文件的完整路径。
    """
    file_paths = []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


# 指定要遍历的文件夹路径
folder_path = r'D:\文档\短视频'

# 调用函数获取所有文件的完整路径
file_paths = list_files_recursively(folder_path)

# 创建一个DataFrame来存储文件路径
df = pd.DataFrame(file_paths, columns=['文件路径'])

# 指定Excel文件的保存路径
excel_path = r'D:\文档\短视频\excel_file.xlsx'

# 将DataFrame写入Excel文件
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f'文件路径已成功写入到 {excel_path}')