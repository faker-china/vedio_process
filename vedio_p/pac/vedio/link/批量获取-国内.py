# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 批量获取-国内.py
# @Time     : 2025-02-09 13:31
# @Software : PyCharm
import requests
from bs4 import BeautifulSoup

# 设置目标网页 URL
url = "https://www.yingshidaquantv.com/vod/57022.html"  # 替换成你想要抓取的网址

# 发送 GET 请求
response = requests.get(url)
if response.status_code == 200:
    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找所有 video 标签或 source 标签
    videos = soup.find_all(['video', 'source'])

    # 提取并存储所有视频链接
    video_urls = []
    for video in videos:
        # 如果是 video 标签，获取其 src 属性
        if video.name == 'video' and video.has_attr('src'):
            video_urls.append(video['src'])
        # 如果是 source 标签，获取其 src 属性
        elif video.name == 'source' and video.has_attr('src'):
            video_urls.append(video['src'])

    # 将视频链接写入文件
    if video_urls:
        with open(r"D:\pythonProject\vedio_p\pac\vedio\link\video_urls.txt", "w") as file:
            for video_url in video_urls:
                file.write(video_url + "\n")
        print(r"视频链接已保存到 'D:\pythonProject\vedio_p\pac\vedio\link\video_urls.txt' 文件中")
    else:
        print("未找到视频链接")
else:
    print(f"请求失败，状态码：{response.status_code}")
