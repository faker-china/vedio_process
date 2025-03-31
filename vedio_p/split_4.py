import os
import subprocess
import logging
from pathlib import Path
import cv2
import concurrent.futures
import time
import threading

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename=os.path.join(log_dir, 'split_4.log'), level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

root_path = r'E:\纪录片处理\去字幕\27'
output_root = r'E:\纪录片处理\切片\四分之一\27'

ffmpeg_path = r'D:\软件\python\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe'
batch_size = 2  # 设定每批处理的视频文件数量


def split_video(video_file):
    logging.info(f"开始处理：{video_file}")
    print(f"开始处理：{video_file}")

    start_time = time.time()  # 记录开始时间

    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frames / fps
    cap.release()

    base_filename = os.path.splitext(os.path.basename(video_file))[0]
    relative_path = os.path.relpath(os.path.dirname(video_file), root_path)
    output_dir = os.path.join(output_root, relative_path, base_filename)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    segment_duration = duration / 4

    for i in range(4):
        start_segment_time = i * segment_duration
        end_segment_time = min((i + 1) * segment_duration, duration)
        output_file = os.path.join(output_dir, f'{base_filename}_segment_{i + 1}.mp4')

        # 构建FFmpeg命令
        command = [
            ffmpeg_path,
            '-y',
            '-ss', str(start_segment_time),
            '-i', video_file,
            '-t', str(end_segment_time - start_segment_time),
            '-c:v', 'copy',  # 使用 copy，避免重新编码
            '-c:a', 'copy',
            '-avoid_negative_ts', '1',
            output_file
        ]
        try:
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
            logging.info(f"成功处理 {video_file} 的片段 {start_segment_time} - {end_segment_time}")
            print(f"成功处理 {video_file} 的片段 {start_segment_time} - {end_segment_time}")
        except subprocess.CalledProcessError as e:
            logging.error(
                f"处理 {video_file} 的片段 {start_segment_time} - {end_segment_time} 时出错: {e.stderr.decode()}")
            print(f"处理 {video_file} 的片段 {start_segment_time} - {end_segment_time} 时出错: {e}")

    end_time = time.time()  # 记录结束时间
    logging.info(f"{video_file} 的处理已完成，耗时 {end_time - start_time:.2f} 秒")
    print(f"{video_file} 的处理已完成，耗时 {end_time - start_time:.2f} 秒")


def process_batch(video_files_batch):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(split_video, video_file) for video_file in video_files_batch]
        concurrent.futures.wait(futures)


def main():
    video_files = []
    root = Path(root_path).resolve()
    exclude_dirs = {'$RECYCLE.BIN', 'System Volume Information', 'Windows', 'Program Files', 'Program Files (x86)'}
    for extension in ('*.mp4', '*.avi', '*.mov', '*.mkv', '*.m4v', '*.WMV', '*.rmvb', '*.DAT', '*.VOB'):
        for file in root.rglob(extension):
            if not any(excluded in file.parts for excluded in exclude_dirs):
                video_files.append(str(file.resolve()))
                print(f"找到视频文件: {file.resolve()}")

    if not video_files:
        raise ValueError("没有找到符合条件的文件")

    start_main_time = time.time()  # 记录主程序开始时间

    # 分批处理视频文件
    for i in range(0, len(video_files), batch_size):
        batch = video_files[i:i + batch_size]
        process_batch(batch)
        print(f"已完成一批处理，共处理 {len(batch)} 个文件")

    end_main_time = time.time()  # 记录主程序结束时间
    logging.info(f"所有视频文件处理完成，总耗时 {end_main_time - start_main_time:.2f} 秒")
    print(f"所有视频文件处理完成，总耗时 {end_main_time - start_main_time:.2f} 秒")


if __name__ == "__main__":
    main()