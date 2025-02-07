import time
import cv2
import moviepy.editor as mp
import glob
from moviepy.editor import (VideoFileClip)
# from moviepy.video.fx.all import resize
import shutil

# 记录开始时间
start_time = time.time()

paths = glob.glob(r'D:\\合格\\*.mp4')  #路径修改1,,,输入路径
# for i in paths:
#     print(i)
# 打开视频文件
def crop_video(input_video_path, output_video_path, x, y, w, h, target_resolution):
    # 加载视频
    clip = mp.VideoFileClip(input_video_path)
    width_ori = clip.w
    height_ori = clip.h
    if clip.h>1080:
        target_width = 1920
        target_height = 1080
        # cropped_clip = clip.crop(x1=x, y1=y, x2=x + w, y2=y + h)
        cropped_clip = clip.crop(x1=x, y1=y, x2=x + w, y2=y + h)

        resized_clip = cropped_clip.resize(newsize=(target_width, target_height))
        # 保存裁剪后的视频
        # cropped_clip.write_videofile(output_video_path, codec='libx264')
        resized_clip.write_videofile(output_video_path, codec='libx264')
    else:
        # 裁剪视频
        print(x,y,w,h)
        target_width = 1920
        target_height = 1080
        # cropped_clip = clip.crop(x1=x, y1=y, x2=x + w, y2=y + h)
        cropped_clip = clip.crop(x1=x, y1=y, x2=x + w, y2=y + h)

        # # 计算需要添加的黑框尺寸  如果裁剪之后小于1080p
        black_top = (target_height - h) // 2
        black_bottom = target_height - h - black_top
        black_left = (target_width - w) // 2
        black_right = target_width - w - black_left

        # 添加黑框
        video_padded = cropped_clip.margin(top=black_top, bottom=black_bottom, left=black_left, right=black_right,
                                            color=(0, 0, 0))
        # resized_clip = cropped_clip.resize(newsize=target_resolution)
        # 保存裁剪后的视频
        video_padded.write_videofile(output_video_path, codec='libx264')



# 调整分辨率
x,y,w,h = 0,0,0,0
for i in range(len(paths)):

    video_path = paths[i]
    cap = cv2.VideoCapture(video_path)
    clip = VideoFileClip(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_width, video_height = clip.size
    print(clip.size)
    if i==0 :
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(frame_count)
        duration = frame_count / fps
        # 输入要提取的帧号
        frame_number = frame_count // 2  # 假设你想提取第100帧

        # 检查帧号是否在有效范围内
        if frame_number >= frame_count or frame_number < 0:
            print("Error: Frame number is out of range.")
            cap.release()
            exit()

        # 设置视频帧位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        # 读取第一帧
        ret, frame = cap.read()

        # 如果视频打开失败
        if not ret:
            print("Failed to open video file.")
            cap.release()
            exit()
        print(frame.shape[0])
        # 选择锚框
        # 将视频帧调整为720p显示
        display_height = 720
        scale_factor = display_height / frame.shape[0]
        display_width = int(frame.shape[1] * scale_factor)
        display_frame = cv2.resize(frame, (display_width, display_height))

        instructions = "Select ROI and press SPACE or ENTER"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(display_frame, instructions, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        r = cv2.selectROI(display_frame)
        # clip_r = r
        # print(r)
        cv2.destroyAllWindows()

        r_original = (
            int(r[0] / scale_factor), int(r[1] / scale_factor), int(r[2] / scale_factor), int(r[3] / scale_factor))
        # r = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
        # cv2.destroyAllWindows()

        x, y, w, h = r_original
        # print(r_original)
        # 函数，用于根据锚框裁剪视频
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # cap.release()

        # 裁剪视频并保存
        target_resolution = (1920, 1080)
        output_video_path = 'D:\\输出\\' + paths[i].split('\\')[-1]  # 路径修改2，，，，，输出路径
        crop_video(video_path, output_video_path, x, y, w, h, target_resolution)
        # 释放视频捕获对象
        cap.release()
        print(f'成功保存了{i + 1}个视频，'
              f'地址为{output_video_path}')



    elif video_height>1080:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(frame_count)
        duration = frame_count / fps
        # 输入要提取的帧号
        frame_number = frame_count // 2  # 假设你想提取第100帧

        # 检查帧号是否在有效范围内
        if frame_number >= frame_count or frame_number < 0:
            print("Error: Frame number is out of range.")
            cap.release()
            exit()

        # 设置视频帧位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        # 读取第一帧
        ret, frame = cap.read()

        # 如果视频打开失败
        if not ret:
            print("Failed to open video file.")
            cap.release()
            exit()
        print(frame.shape[0])
        # 选择锚框
        # 将视频帧调整为720p显示
        display_height = 720
        scale_factor = display_height / frame.shape[0]
        display_width = int(frame.shape[1] * scale_factor)
        display_frame = cv2.resize(frame, (display_width, display_height))

        instructions = "Select ROI and press SPACE or ENTER"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(display_frame, instructions, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        r = cv2.selectROI(display_frame)
        # clip_r = r
        # print(r)
        cv2.destroyAllWindows()

        r_original = (
            int(r[0] / scale_factor), int(r[1] / scale_factor), int(r[2] / scale_factor), int(r[3] / scale_factor))
        # r = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
        # cv2.destroyAllWindows()

        x1, y1, w1, h1 = r_original
        # print(r_original)
        # 函数，用于根据锚框裁剪视频
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # cap.release()

        # 裁剪视频并保存
        target_resolution = (1920, 1080)
        output_video_path = 'D:\\输出\\' + paths[i].split('\\')[-1]  # 路径修改3，，，，，输出路径
        crop_video(video_path, output_video_path, x1, y1, w1, h1, target_resolution)
        # 释放视频捕获对象
        cap.release()
        print(f'成功保存了{i + 1}个视频，'
              f'地址为{output_video_path}')
    else:
        # video_path = r'D:\b站\【8K视觉】航拍冰岛火山，熔岩喷发的场面太刺激了......-out.mp4'
        # cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(frame_count)
        duration = frame_count / fps
        # 输入要提取的帧号
        frame_number = frame_count // 2  # 假设你想提取第100帧

        # 检查帧号是否在有效范围内
        if frame_number >= frame_count or frame_number < 0:
            print("Error: Frame number is out of range.")
            cap.release()
            exit()

        # 设置视频帧位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        # 读取第一帧
        ret, frame = cap.read()
        scale_factor = 720 / frame.shape[0]
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # cap.release()
        # r_original = (
        #     int(clip_r[0] / scale_factor), int(clip_r[1] / scale_factor), int(clip_r[2] / scale_factor), int(clip_r[3] / scale_factor))
        # # r = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
        # # cv2.destroyAllWindows()
        #
        # x, y, w, h = r_original

        # 裁剪视频并保存
        target_resolution = (1920, 1080)
        output_video_path = 'D:\\输出\\'+paths[i].split('\\')[-1] #路径修改4，，，，输出路径

        crop_video(video_path, output_video_path, x, y, w, h, target_resolution)
        # 释放视频捕获对象
        cap.release()
        print(f'成功保存了{i+1}个视频，'
              f'地址为{output_video_path}')

# 记录结束时间
end_time = time.time()

# 计算运行时间
elapsed_time = end_time - start_time
print(f'代码运行时间为：{elapsed_time}秒')