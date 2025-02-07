import os
import time
import shutil
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import concurrent.futures

def save_video(file_input_path, file_output_dir):
    if not file_output_dir:
        base, ext = os.path.splitext(file_input_path)
        file_output_path = f"{base}_compressed{ext}"
    file_input_dir = os.path.dirname(file_input_path)
    base, ext = os.path.splitext(file_input_path)
    relative_path = os.path.relpath(file_input_path, os.path.dirname(file_input_dir))
    output_dir = os.path.join(file_output_dir, relative_path)
    os.makedirs(output_dir, exist_ok=True)  # 创建输出目录（如果已存在则忽略）
    file_output_path = os.path.join(output_dir, f"{os.path.basename(base)}_compressed{ext}")

    fpsize = os.path.getsize(file_input_path) / 1024
    if fpsize >= 1048576.0:  # 如果文件大于150KB，则进行压缩
        ffmpeg_path = r'D:\软件\python\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe'
        compress_cmd = f"{ffmpeg_path} -i {file_input_path} -r 15 -pix_fmt yuv420p -vcodec libx264 -preset veryfast -profile:v baseline -crf 35 -acodec aac -b:a 64k {file_output_path}"
        os.system(compress_cmd)  # 注意：这里简化了错误处理，实际使用中应该更详细
        return True
    else:
        return True  # 文件太小，不需要压缩，但这里可以返回一个标志或进行其他处理


def batch_compress_videos(folder_path, output_base_dir, max_workers=4):
    start_time = time.time()

    # 创建一个新目录来存放压缩后的视频
    output_dir = os.path.join(output_base_dir, "compressed_videos")
    os.makedirs(output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    file_path = os.path.join(root, file)
                    print(f"已提交文件到线程池处理: {file_path}")
                    future = executor.submit(save_video, file_path, output_dir)
                    futures.append(future)

                    # 等待所有任务完成（可选）
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # 这里我们假设save_video函数有返回值或抛出异常
            except Exception as exc:
                print(f"处理文件时发生错误: {exc}")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"总共耗时: {total_time:.2f} 秒")


if __name__ == "__main__":
    folder_to_compress = r'E:\待压缩筛选Logo\袁\综艺\吃瓜影视\综艺\中国大陆\喜人奇妙夜'
    output_base_dir = r'E:\压缩后的视频'
    max_workers = 4  # 可以根据CPU核心数调整这个值
    batch_compress_videos(folder_to_compress, output_base_dir, max_workers)