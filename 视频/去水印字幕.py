# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 去水印字幕.py
# @Time     : 2024/10/18 上午9:03
# @Software : PyCharm
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from keras.models import load_model

def remove_watermark(video_path, output_path):
    # 加载预训练的模型
    model = load_model('watermark_detection_model.h5')

    # 读取视频文件
    clip = VideoFileClip(video_path)

    # 创建一个与视频大小相同的黑色背景图像
    background = np.zeros((clip.h, clip.w, 3), dtype=np.uint8)

    # 将黑色背景图像转换为视频剪辑
    background_clip = ImageSequenceClip([background] * int(clip.duration * clip.fps), fps=clip.fps)

    # 遍历视频的每一帧
    for frame in clip.iter_frames():
        # 使用模型检测水印区域
        watermark_mask = model.predict(frame)

        # 将检测到的水印区域从原始帧中去除
        frame[watermark_mask > 0.5] = [0, 0, 0]

    # 将处理后的帧合并为一个新的视频剪辑
    final_clip = CompositeVideoClip([background_clip, clip])

    # 保存处理后的视频
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    video_path = r"D:\素菜库\1.mp4"
    output_path = r"D:\素菜库\输出"

    # 去除水印
    remove_watermark(video_path, output_path)
