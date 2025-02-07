from moviepy.editor import VideoFileClip


def cut_video_into_chunks(video_path, chunk_duration_seconds=10, output_folder='D:/文档/EV录屏/处理过的文件/炼爱'):
    """
    将视频切割成多个指定长度的片段。

    :param video_path: w输入视频文件的路径
    :param chunk_duration_seconds: 每个片段的持续时间（秒），这里确保是20秒以上
    :param output_folder: 输出片段的文件夹路径
    """
    # 加载视频文件
    video = VideoFileClip(video_path)

    # 计算视频总长度
    video_duration = video.duration

    # 确保输出文件夹存在
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 初始化片段计数器
    chunk_number = 1

    # 计算起始时间和结束时间，确保每个片段至少为20秒
    start_time = 0
    while start_time < video_duration:
        end_time = min(start_time + chunk_duration_seconds, video_duration)

        # 切割片段
        chunk = video.subclip(start_time, end_time)

        # 构造输出文件的名称
        output_file_path = os.path.join(output_folder, f'炼爱_{chunk_number:03d}.mp4')

        # 导出片段
        chunk.write_videofile(output_file_path, codec='libx264')

        # 更新起始时间和片段计数器
        start_time = end_time
        chunk_number += 1

video_path = 'D:/文档/EV录屏/源文件/02/炼爱.mp4'  # 替换为你的视频文件路径
cut_video_into_chunks(video_path, chunk_duration_seconds=10)  # 调用函数，这里每个片段至少20秒

#输入路径模板D:/文档/EV录屏/新建文件夹/奥斯威辛集中营.mp4
#输出D:/文档/EV录屏/新建文件夹/奥斯威辛集中营