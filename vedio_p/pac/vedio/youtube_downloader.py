import os
import subprocess
import time
import random
import logging
import sys
import concurrent.futures
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm

# 配置日志
def setup_logging(log_file):
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    console_handler.setLevel(logging.INFO)
    console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8')
    logging.getLogger().addHandler(console_handler)

# 安全文件名处理
def sanitize_filename(filename):
    invalid_chars = r'[\\/*?:"<>|]'
    return re.sub(invalid_chars, '_', filename)

# 动态代理配置
def set_proxy(proxy):
    if proxy:
        os.environ["HTTP_PROXY"] = proxy
        os.environ["HTTPS_PROXY"] = proxy

# 生成唯一文件名，避免文件覆盖
def generate_unique_filename(title, ext):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_title = sanitize_filename(title)
    return f"{safe_title}_{timestamp}.{ext}"

# 下载 YouTube 视频
def download_youtube_video(url, output_path, keep_original, retries=0, proxy=None):
    video_id = parse_qs(urlparse(url).query).get('v', [None])[0]
    if not video_id:
        logging.error(f"❌ 无效的视频链接: {url}")
        return False

    # 检查是否已经下载过
    for file in os.listdir(output_path):
        if video_id in file:
            logging.info(f"📌 视频 {url} 已下载，跳过。")
            return True

    max_retries = 3
    backoff_base = 2
    while retries < max_retries:
        try:
            command = [
                "yt-dlp",
                "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
                "--merge-output-format", "mp4",
                "--write-thumbnail",
                "--add-metadata",
                "-o", os.path.join(output_path, generate_unique_filename("%(title)s", "%(ext)s")),
                "--progress",  # 启用进度信息输出
                "--continue",  # 开启断点续传
                "-v"
            ]

            if proxy:
                command.extend(["--proxy", proxy])
            if keep_original:
                command.append("-k")

            command.append(url)

            logging.info(f"开始下载: {url}")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')

            download_pbar = None
            merge_pbar = None
            for line in process.stdout:
                if "[download]" in line:
                    parts = line.split()
                    if len(parts) >= 6:
                        try:
                            percent = float(parts[1].strip('%'))
                            speed = parts[3]
                            eta = parts[5]
                            if download_pbar is None:
                                download_pbar = tqdm(total=100, desc=f"下载 {url}", unit="%", ncols=100)
                            download_pbar.n = percent
                            # 解析速度信息，转换为统一的可读格式
                            if speed.endswith('KiB/s'):
                                speed_value = float(speed[:-5])
                                speed_str = f"{speed_value:.2f} KB/s"
                            elif speed.endswith('MiB/s'):
                                speed_value = float(speed[:-5])
                                speed_str = f"{speed_value:.2f} MB/s"
                            else:
                                speed_str = speed
                            download_pbar.set_postfix({"速度": speed_str, "剩余时间": eta})
                            download_pbar.refresh()
                        except ValueError:
                            pass
                elif "[Merger]" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            merge_percent = float(parts[2].strip('%'))
                            if merge_pbar is None:
                                merge_pbar = tqdm(total=100, desc=f"合成 {url}", unit="%", ncols=100)
                            merge_pbar.n = merge_percent
                            merge_pbar.refresh()
                        except ValueError:
                            pass

            if download_pbar:
                download_pbar.close()
            if merge_pbar:
                merge_pbar.close()

            process.wait()
            if process.returncode == 0:
                logging.info(f"✅ 视频下载完成！{url}")
                return True
            else:
                if "HTTP Error 429" in process.stdout.read():
                    logging.warning(f"⚠️ 下载 {url} 时遇到 429 错误，等待后重试...")
                else:
                    logging.error(f"⚠️ 视频下载失败，请检查网络或代理设置！{url}")
                    logging.error(f"错误信息: {process.stdout.read()}")
        except Exception as e:
            logging.error(f"❌ 发生错误: {e}")

        wait_time = random.uniform(backoff_base ** retries, backoff_base ** (retries + 1))
        logging.info(f"⏳ 等待 {wait_time:.2f} 秒后重试... (第 {retries + 1} 次重试)")
        time.sleep(wait_time)
        retries += 1

    logging.error(f"❌ 下载 {url} 失败，达到最大重试次数。")
    return False

# 从 txt 文件中提取 YouTube 视频链接
def extract_video_links_from_txt(txt_file):
    links = []
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f.readlines() if line.strip()]

        if not links:
            logging.warning("未从 txt 文件中提取到有效的视频链接！")

        return links

    except Exception as e:
        logging.error(f"读取 txt 文件时发生错误: {e}")
        return []

# 获取 YouTube 视频链接
def get_youtube_video_links(query, output_file, max_results=10, proxy=None):
    try:
        command = [
            "yt-dlp",
            "--proxy", proxy if proxy else "http://127.0.0.1:7890",
            f"ytsearch{max_results}:{query}",
            "--get-id"
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            video_ids = result.stdout.strip().split("\n")
            if not video_ids:
                logging.warning("⚠️ 未能找到任何视频链接！")
                return []

            video_links = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            mode = "a" if os.path.exists(output_file) else "w"
            with open(output_file, mode, encoding="utf-8") as f:
                f.write("\n".join(video_links) + "\n")

            logging.info(f"✅ 成功获取 {len(video_links)} 个视频链接！")
            return video_links
        else:
            logging.error("⚠️ 获取视频链接失败，请检查网络或代理设置！")
            logging.error(f"错误信息: {result.stderr}")
            return []

    except Exception as e:
        logging.error(f"❌ 发生错误: {e}")
        return []

if __name__ == "__main__":
    default_output_path = r"D:\素菜库\youtube\vedio\result"
    OUTPUT_PATH = input(f"请输入输出路径（默认 {default_output_path}）：")
    if not OUTPUT_PATH:
        OUTPUT_PATH = default_output_path
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    default_log_file = r"D:\pythonProject\vedio_p\pac\vedio\logs\download_log.txt"
    LOG_FILE = input(f"请输入日志文件路径（默认 {default_log_file}）：")
    if not LOG_FILE:
        LOG_FILE = default_log_file

    KEEP_ORIGINAL_FILES = input("是否保留原始文件？(y/n, 默认 n)：").lower() == 'y'
    PROXY = input(f"请输入代理设置（默认 {r'http://127.0.0.1:7890'}）：")
    if not PROXY:
        PROXY = r'http://127.0.0.1:7890'

    CONCURRENCY = input("请输入并发下载数量（默认 3）：")
    try:
        CONCURRENCY = int(CONCURRENCY) if CONCURRENCY else 3
    except ValueError:
        CONCURRENCY = 3

    setup_logging(LOG_FILE)
    set_proxy(PROXY)

    while True:
        choice = input("请选择操作方式：1. 关键词搜索下载 2. 直接输入链接下载：")
        if choice == '1':
            SEARCH_QUERY = input("请输入搜索关键词：")
            while True:
                try:
                    MAX_RESULTS = int(input("请输入最大搜索结果数量："))
                    break
                except ValueError:
                    print("输入无效，请输入一个整数。")

            output_file_name = f"youtube_{SEARCH_QUERY.replace(' ', '_')}_links.txt"
            OUTPUT_FILE = os.path.join(r"D:\pythonProject\vedio_p\pac\vedio\link", output_file_name)

            links = get_youtube_video_links(SEARCH_QUERY, OUTPUT_FILE, max_results=MAX_RESULTS, proxy=PROXY)
            video_links = extract_video_links_from_txt(OUTPUT_FILE)
            break
        elif choice == '2':
            input_links = input("请输入要下载的 YouTube 视频链接，多个链接用逗号分隔：").split(',')
            video_links = [link.strip() for link in input_links]
            break
        else:
            print("输入无效，请输入 1 或 2。")

    if video_links:
        logging.info(f"准备下载 {len(video_links)} 个视频链接")
        success_count = 0
        failed_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            future_to_url = {executor.submit(download_youtube_video, url, OUTPUT_PATH, KEEP_ORIGINAL_FILES, proxy=PROXY): url for url in video_links}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as exc:
                    logging.error(f'%r generated an exception: %s' % (url, exc))
                    failed_count += 1

        logging.info(f"下载统计：成功 {success_count} 个，失败 {failed_count} 个。")
    else:
        logging.warning("没有有效的视频链接，无法进行下载。")