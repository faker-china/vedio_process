import os
import subprocess
import logging
from pathlib import Path
import cv2
import concurrent.futures
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename=os.path.join(log_dir, 'split_videos.log'), level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

root_path = r'E:\待压缩筛选Logo\袁'
output_root = r'E:\待压缩筛选Logo\切片完成文件夹'

segment_duration = 10
ffmpeg_path = r'D:\软件\python\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe'
#D:\ffmepg\ffmpeg-7.0.1-essentials_build\bin
retry_interval = 10  # 重试间隔，单位：秒
max_retries = 5  # 最大重试次数

# 用于跟踪尝试处理但失败的视频文件及其重试次数（这里不再需要，因为不再使用VideoCapture）
# failed_videos = {}

# 创建一个全局线程池
executor = concurrent.futures.ThreadPoolExecutor()


def split_video(video_file):
    logging.info(f"开始处理：{video_file}")
    print(f"开始处理：{video_file}")

    # 提取文件名和路径信息
    base_filename = os.path.splitext(os.path.basename(video_file))[0]
    relative_path = os.path.relpath(os.path.dirname(video_file), root_path)
    output_dir = os.path.join(output_root, relative_path, base_filename)

    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

        # 假设我们知道每个片段的长度（这里我们直接设置）
    # 注意：在实际应用中，您可能需要先运行一个 FFmpeg 命令来获取视频的总时长
    # 但为了简化，我们这里假设总时长是 segment_duration 的整数倍

    # 这里我们简单地按时间段分割视频，不考虑精确到帧的分割
    num_segments = 10  # 假设值，实际应用中需要根据视频总时长计算

    # 切片视频
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, 60 * num_segments)  # 假设总时长为60秒*num_segments
        output_file = os.path.join(output_dir, f'{base_filename}_segment_{i + 1}.mp4')

        # 构建FFmpeg命令
        command = [
            ffmpeg_path,
            '-y',
            '-i', video_file,
            '-ss', str(start_time),
            '-t', str(end_time - start_time),
            '-c:v', 'copy',  # 如果不需要重新编码视频流，可以使用 copy
            '-c:a', 'copy',  # 同样，如果不需要重新编码音频流
            output_file
        ]

        try:
            # 执行FFmpeg命令
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
            logging.info(f"成功处理 {video_file} 的片段 {start_time} - {end_time}")
            print(f"成功处理 {video_file} 的片段 {start_time} - {end_time}")
        except subprocess.CalledProcessError as e:
            logging.error(f"处理 {video_file} 的片段 {start_time} - {end_time} 时出错: {e.stderr.decode()}")
            print(f"处理 {video_file} 的片段 {start_time} - {end_time} 时出错: {e}")

            # 注意：这里不再删除原始视频文件，因为我们没有精确计算视频的总时长和片段数量
    # 如果您确实需要删除原始文件，请确保在分割完所有片段后再执行删除操作

    logging.info(f"{video_file} 的处理已完成")
    print(f"{video_file} 的处理已完成")


def on_created(event):
    global executor
    if event.is_directory:
        return

        # 定义视频文件扩展名集合
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.wmv', '.rmvb', '.dat', '.vob'}

    # 获取文件的扩展名（包括点）并转换为小写
    _, file_ext = os.path.splitext(event.src_path)
    if file_ext.lower() in video_extensions:
        video_path = event.src_path

        # 尝试打开视频文件以验证其有效性（可选，但可以提高程序的健壮性）
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logging.error(f"无法打开新创建的视频文件：{video_path}")
                return
            cap.release()
        except Exception as e:
            logging.error(f"尝试打开新创建的视频文件时出错：{video_path}, 错误：{e}")
            return

            # 将视频文件提交到线程池处理
        try:
            executor.submit(split_video, video_path)
        except Exception as e:
            logging.error(f"无法将新创建的视频文件提交到线程池处理：{video_path}, 错误：{e}")


def main():
    global executor
    video_files = []

    root = Path(root_path).resolve()
    exclude_dirs = {'$RECYCLE.BIN', 'System Volume Information', 'Windows',
                    'Program Files', 'Program Files (x86)'}

    # 扫描并收集所有已存在的视频文件
    for extension in ('*.mp4', '*.avi', '*.mov', '*.mkv', '*.m4v', '*.WMV', '*.rmvb', '*.DAT', '*.VOB'):
        for file in root.rglob(extension):
            if not any(excluded in file.parts for excluded in exclude_dirs):
                video_files.append(str(file.resolve()))

    # 使用全局线程池处理已存在的视频文件
    for video_file in video_files:
        executor.submit(split_video, video_file)

        # 现在启动文件系统观察者来监控新文件的创建
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, root_path, recursive=True)
    observer.start()

    try:
        # 主循环，保持程序运行以监控新文件
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # 在程序退出前关闭线程池（注意：这一步在正常情况下可能不是必需的，
    # 因为程序退出时Python解释器会自动清理资源。但显式关闭是一个好习惯。）
    executor.shutdown(wait=True)

    logging.info("所有视频处理完毕（包括初始扫描和后续监控）")
    print("所有视频处理完毕（包括初始扫描和后续监控）")


if __name__ == "__main__":
    main()
