# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 统计时长.py
# @Time     : 2024/10/21 下午2:47
# @Software : PyCharm

import subprocess
import os
import time
from tqdm import tqdm

start_time = time.time()


def get_video_duration(file_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
         file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)


def calculate_total_duration(folder_path):
    total_duration = 0
    all_files = []
    # 第一次遍历收集所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    total_files = len(all_files)

    with tqdm(total=total_files, desc="处理视频", unit="文件") as pbar:
        for file_path in all_files:
            if file_path.endswith(('.mp4', '.avi', '.mkv', '.flv', '.mov')):
                duration = get_video_duration(file_path)
                total_duration += duration
            pbar.update(1)
    return total_duration


folder_path = r"E:\未处理"  # 替换为你的文件夹路径
total_duration = calculate_total_duration(folder_path)
print("文件夹中所有视频的总时长：", total_duration, "秒")

end_time = time.time()
elapsed_time = end_time - start_time
print("耗时：", elapsed_time, "秒")
