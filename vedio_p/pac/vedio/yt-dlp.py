import os
import subprocess
import time
import random
import logging
import sys
import argparse
from datetime import datetime


# 设置代理（适用于 Clash 代理）
def set_proxy():
    try:
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
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


# 设置代理
set_proxy()

# 配置下载目录
OUTPUT_PATH = r"D:\素菜库\youtube\vedio\result"
os.makedirs(OUTPUT_PATH, exist_ok=True)  # 确保目录存在

# 配置日志
LOG_FILE = r"D:\pythonProject\vedio_p\pac\vedio\logs\download_log.txt"
setup_logging(LOG_FILE)  # 配置日志

# 是否保留原始文件（True: 保留，False: 删除）
KEEP_ORIGINAL_FILES = False

# 最大重试次数
MAX_RETRIES = 3


# 生成唯一文件名，避免文件覆盖
def generate_unique_filename(title, ext):
    """生成唯一的文件名，避免覆盖"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{title}_{timestamp}.{ext}"


# 下载 YouTube 视频
def download_youtube_video(url, retries=0):
    """使用 yt-dlp 下载最高质量的 MP4 视频"""
    try:
        # 构建 yt-dlp 下载命令
        command = [
            "yt-dlp",
            "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",  # 选择最高质量的 MP4 + M4A
            "--merge-output-format", "mp4",
            "-o", os.path.join(OUTPUT_PATH, generate_unique_filename("%(title)s", "%(ext)s")),
            "-q",  # quiet 模式，减少输出
            "-v",  # verbose 模式，增加详细输出
        ]

        if KEEP_ORIGINAL_FILES:
            command.append("-k")  # 保留原始音视频文件

        command.append(url)

        logging.info(f"开始下载: {url}")
        print(f"开始下载: {url}")
        result = subprocess.run(command, shell=True)

        if result.returncode == 0:
            logging.info(f"✅ 视频下载完成！{url}")
            print(f"✅ 视频下载完成！{url}")
        else:
            logging.error(f"⚠️ 视频下载失败，请检查网络或代理设置！{url}")
            print(f"⚠️ 视频下载失败，请检查网络或代理设置！{url}")

    except Exception as e:
        logging.error(f"❌ 发生错误: {e}")
        print(f"❌ 发生错误: {e}")
        if retries < MAX_RETRIES:
            wait_time = random.randint(5, 15)  # 随机等待时间，避免频繁重试
            logging.info(f"⏳ 等待 {wait_time} 秒后重试... (第 {retries + 1} 次重试)")
            print(f"⏳ 等待 {wait_time} 秒后重试... (第 {retries + 1} 次重试)")
            time.sleep(wait_time)
            download_youtube_video(url, retries + 1)  # 重试


# 从txt文件中提取 YouTube 视频链接
def extract_video_links_from_txt(txt_file):
    links = []
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f.readlines() if line.strip()]

        if not links:
            logging.warning("未从txt文件中提取到有效的视频链接！")
            print("未从txt文件中提取到有效的视频链接！")

        return links

    except Exception as e:
        logging.error(f"读取txt文件时发生错误: {e}")
        print(f"读取txt文件时发生错误: {e}")
        return []


if __name__ == "__main__":
    # 读取txt文件并提取视频链接
    txt_file = r"D:\pythonProject\vedio_p\pac\vedio\link\youtube_funny_links.txt"  # 你的txt文件路径
    video_links = extract_video_links_from_txt(txt_file)

    if video_links:
        print(f"准备下载 {len(video_links)} 个视频链接")
        for link in video_links:
            download_youtube_video(link)  # 下载提取的每个视频链接
    else:
        print("没有找到视频链接，无法进行下载。")
