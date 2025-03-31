# from moviepy.editor import VideoFileClip
# import os
#
# # 输入和输出目录
# input_dir = r'D:\中广新媒体\电信视频\test'
# output_dir = r'D:\中广新媒体\电信视频\test_result'
#
# # 确保输出目录存在
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
#
# # 遍历输入目录中的所有视频文件
# for filename in os.listdir(input_dir):
#     if filename.endswith(('.mp4', '.avi', '.mov')):  # 检查文件扩展名
#         file_path = os.path.join(input_dir, filename)
#         clip = VideoFileClip(file_path)
#
#         # 将视频分辨率设置为1080P
#         clip_resized = clip.resize(height=1080)
#
#         # 构造输出文件路径
#         output_file_path = os.path.join(output_dir, filename)
#
#         # 写入转换后的视频文件
#         clip_resized.write_videofile(output_file_path, codec='libx264')  # 使用H.264编码
#
# print("所有视频已成功转换为1080P分辨率。")
import os
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from shutil import copyfile
import threading

# 输入和输出根目录
input_root_dir = r'F:\01\3'
output_root_dir = r'F:\test_result'
# 线程池大小
thread_pool_size = 2

# 确保输出根目录存在
if not os.path.exists(output_root_dir):
    os.makedirs(output_root_dir)


# 定义转换函数
def convert_video(input_file, output_file):
    # 使用FFmpeg进行转换
    subprocess.run([
        'ffmpeg', '-i', input_file,
        '-vf', 'scale=1920:1080:flags=lanczos',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
        '-c:a', 'copy', output_file
    ])


# 遍历输入根目录及其子目录中的所有视频文件
def find_video_files(root_dir):
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv','.m4v','.WMV','.rmvb','.DAT','.VOB')):
                all_files.append(os.path.join(root, file))
    return all_files


# 主函数
def main():
    # 获取所有视频文件
    video_files = find_video_files(input_root_dir)

    # 使用线程池进行视频转换
    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        futures = []
        for input_file in tqdm(video_files, desc='正在转换视频', unit='文件'):
            # 提取文件名和扩展名
            name, extension = os.path.splitext(os.path.basename(input_file))

            # 构造输出目录和文件路径
            relative_path = os.path.relpath(input_file, input_root_dir)
            output_dir = os.path.join(output_root_dir, os.path.dirname(relative_path))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, f"{name}_1080p{extension}")

            # 提交转换任务到线程池
            future = executor.submit(convert_video, input_file, output_file)
            futures.append(future)

            # 输出正在处理的文件信息
            print(f"正在处理文件：{relative_path}")

            # 等待所有任务完成
        for future in tqdm(futures, desc='等待任务完成', unit='任务'):
            future.result()

    print("所有视频已成功转换为1080P分辨率。")


# 运行主函数
if __name__ == "__main__":
    main()