import os
import shutil
import subprocess
import re

def get_video_resolution(video_path):
    # 使用 ffprobe 命令获取视频分辨率信息
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', video_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    # 检查命令执行是否成功
    if result.returncode != 0:
        print("ffprobe 命令执行失败:", result.stderr)
        return None, None

    # 解析输出，提取宽度和高度信息
    output = result.stdout.strip()
    match = re.match(r'(\d+)\s*,\s*(\d+)', output)
    if match:
        width = int(match.group(1))
        height = int(match.group(2))
        return width, height
    else:
        print("未能从输出中提取宽度和高度:", output)
        return None, None

def copy_high_res_videos(filepath, outputfile):
    """复制高分辨率视频到指定目录的同名子文件夹中"""
    for root, dirs, files in os.walk(filepath):
        # 获取当前子文件夹相对于filepath的相对路径
        rel_path = os.path.relpath(root, filepath)
        # 构建outputfile中对应的子文件夹路径
        output_subfolder = os.path.join(outputfile, rel_path)

        # 如果该子文件夹在outputfile中不存在，则创建它
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm')):
                video_path = os.path.join(root, file)
                width, height = get_video_resolution(video_path)
                if width and height and min(width, height) >= 1080:
                    # 构建outputfile中对应文件的完整路径
                    output_video_path = os.path.join(output_subfolder, file)
                    shutil.move(video_path, output_video_path)
                    print(f"Moved {video_path} to {output_video_path}")


filepath = r'F:\01'  # 修改为你的视频文件夹路径
outputfile = r'F:\01_1080'  # 修改为你的输出文件夹路径
if not os.path.exists(outputfile):
    os.makedirs(outputfile)

copy_high_res_videos(filepath, outputfile)