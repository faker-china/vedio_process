# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 合并文件夹下的文件到指定目录.py
# @Time     : 2024/12/12 下午8:55
# @Software : PyCharm
import shutil
import os

# 源文件夹所在的根目录，可根据实际情况修改
source_root_dir = r"D:\BaiduNetdiskDownload\Vol.103奈汐酱nice"
# 目标文件夹，即要合并文件到的指定目录，可根据实际情况修改
target_dir = r"D:\BaiduNetdiskDownload\Vol.103奈汐酱nice"

# 遍历源文件夹根目录下的所有子文件夹
for root, dirs, files in os.walk(source_root_dir):
    for file in files:
        # 构建源文件的完整路径
        source_file_path = os.path.join(root, file)
        # 构建目标文件的完整路径，直接将文件复制到目标目录下
        target_file_path = os.path.join(target_dir, file)
        try:
            shutil.move(source_file_path, target_file_path)
            print(f"已成功将 {source_file_path} 复制到 {target_file_path}")
        except shutil.SameFileError:
            print(f"{source_file_path} 和 {target_file_path} 是同一个文件，跳过复制。")
        except Exception as e:
            print(f"复制文件 {source_file_path} 时出现错误: {str(e)}")