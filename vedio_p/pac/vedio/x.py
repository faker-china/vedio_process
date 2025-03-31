# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : x.py
# @Time     : 2025-02-09 13:12
# @Software : PyCharm
import os
import subprocess
import time
import random
import logging
import sys
import argparse
from datetime import datetime

# 设置代理
def set_proxy(proxy_url):
    try:
        if proxy_url:
            os.environ["HTTP_PROXY"] = proxy_url
            os.environ["HTTPS_PROXY"] = proxy_url
            logging.info(f"✅ 代理设置成功: {proxy_url}")
        else:
            logging.warning("❌ 未设置代理")
    except Exception as e:
        logging.warning(f"❌ 代理设置失败: {e}")

# 配置日志
def setup_logging(log_file):
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))  # 创建日志文件目录
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True  # 强制重新配置日志
    )
    # 设置控制台输出的编码为 UTF-8
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    console_handler.setLevel(logging.INFO)
    console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8')  # 设置控制台输出流为 UTF-8 编码
    logging.getLogger().addHandler(console_handler)

# 配置下载目录
OUTPUT_PATH = r"D:\素菜库\youtube\vedio\result\马斯克"
os.makedirs(OUTPUT_PATH, exist_ok=True)  # 确保目录存在

# 直接在代码中粘贴多个 YouTube 视频链接（支持批量下载）
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=x__y5w3KSr0"
]

# 是否保留原始文件（True: 保留，False: 删除）
KEEP_ORIGINAL_FILES = False

# 最大重试次数
MAX_RETRIES = 3

# 配置日志
LOG_FILE = r"D:\pythonProject\vedio_p\pac\vedio\logs\download_log.txt"
setup_logging(LOG_FILE)  # 配置日志

# 生成唯一文件名，避免文件覆盖
def generate_unique_filename(title, ext):
    """生成唯一的文件名，避免覆盖"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{title}_{timestamp}.{ext}"

# 下载 YouTube 视频
def download_youtube_video(url, retries=0):
    """使用 yt-dlp 下载 YouTube 视频"""
    try:
        # 构建 yt-dlp 下载命令
        command = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",  # 选择最佳视频和音频流，或者最佳格式
            "--merge-output-format", "mp4",
            "-o", os.path.join(OUTPUT_PATH, generate_unique_filename("%(title)s", "%(ext)s")),
            "-q",  # quiet 模式，减少输出
            "-v",  # verbose 模式，增加详细输出
            "--ffmpeg-location",
            "D:\\浏览器下载\\ffmpeg-7.0.1-essentials_build\\ffmpeg-7.0.1-essentials_build\\bin\\ffmpeg.exe",
            # 指定 ffmpeg 位置
            "--postprocessor-args", "ffmpeg:-strict -2"  # 允许使用实验性特性
        ]

        if KEEP_ORIGINAL_FILES:
            command.append("-k")  # 保留原始音视频文件

        command.append(url)

        logging.info(f"开始下载: {url}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            logging.info(f"✅ 视频下载完成！{url}")
        else:
            logging.error(f"⚠️ 视频下载失败，请检查网络或代理设置！{url}")
            logging.error(f"错误信息: {result.stderr}")

    except Exception as e:
        logging.error(f"❌ 发生错误: {e}")
        if retries < MAX_RETRIES:
            wait_time = random.randint(5, 15)  # 随机等待时间，避免频繁重试
            logging.info(f"⏳ 等待 {wait_time} 秒后重试... (第 {retries + 1} 次重试)")
            time.sleep(wait_time)
            download_youtube_video(url, retries + 1)  # 重试

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube 视频下载器")
    parser.add_argument(
        "--output", default=OUTPUT_PATH, help="视频下载目录（默认: D:/素菜库/youtube/vedio/result）"
    )
    parser.add_argument(
        "--urls", nargs="+", default=VIDEO_URLS, help="YouTube 视频链接（多个视频链接用空格分隔）"
    )
    parser.add_argument(
        "--proxy", default="http://127.0.0.1:7890", help="代理地址（默认: http://127.0.0.1:7890）"
    )
    args = parser.parse_args()

    OUTPUT_PATH = args.output
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    set_proxy(args.proxy)

    for url in args.urls:
        download_youtube_video(url)  # 遍历列表，依次下载所有 YouTube 视频