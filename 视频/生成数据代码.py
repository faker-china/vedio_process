# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 生成数据代码.py
# @Time     : 2024/12/8 上午12:14
# @Software : PyCharm
import cv2
import numpy as np
import random
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# 随机选择文本水印
def get_random_watermark():
    watermarks = [
        "Sample Watermark", "Confidential", "Private", "Demo", "Brand", "Top Secret",
        "Company X", "Internal Use Only", "Restricted", "Do Not Share", "For Testing Only",
        "Exclusive", "Confidential Information", "Project XYZ", "Draft", "For Review",
        "Property of Company", "Beta Version", "Not for Distribution", "Proprietary Information",
        "Company Confidential", "Authorized Use Only", "Watermarked", "Confidential Draft",
        "For Official Use", "Top Priority", "Internal Document", "Sample Content",
        "Private Property", "Confidential Data", "Proprietary Content", "Work in Progress",
        "Not Final", "In Review", "Copyrighted", "Sensitive", "Do Not Copy", "Company Confidential"
    ]
    return random.choice(watermarks)

# 随机选择图像水印
def get_random_image_watermark(watermark_images):
    return random.choice(watermark_images)

# 随机选择水印位置
def get_random_position(image, text_width, text_height):
    max_x = image.width - text_width
    max_y = image.height - text_height
    return (random.randint(0, max_x), random.randint(0, max_y))

# 计算图像的平均亮度
def calculate_image_brightness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    return brightness

# 根据亮度自动调整透明度
def adjust_opacity_based_on_brightness(brightness, min_opacity=50, max_opacity=200):
    opacity = min_opacity + (brightness / 255.0) * (max_opacity - min_opacity)
    return int(opacity)

# 使用 OpenCV 加速图像处理：调整透明度并合成水印
def add_text_watermark_opencv(image, watermark_text, opacity=128):
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGRA)

    # 使用 OpenCV 绘制水印
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = random.randint(1, 2)
    thickness = random.randint(1, 3)
    text_size = cv2.getTextSize(watermark_text, font, scale, thickness)[0]
    position = get_random_position(image, text_size[0], text_size[1])

    # 添加文本水印
    cv2.putText(image_cv, watermark_text, position, font, scale, (255, 255, 255, opacity), thickness)

    return image_cv

# 使用 OpenCV 加速图像处理：添加图像水印
def add_image_watermark_opencv(image, watermark_image_path, opacity=128):
    watermark = cv2.imread(watermark_image_path, cv2.IMREAD_UNCHANGED)

    if watermark is None:
        print(f"Error loading watermark image: {watermark_image_path}")
        return image  # 返回原始图片，避免继续处理

    if watermark.shape[2] == 3:
        alpha_channel = np.ones((watermark.shape[0], watermark.shape[1]), dtype=watermark.dtype) * 255
        watermark = np.dstack((watermark, alpha_channel))

    # 调整水印透明度
    watermark[:, :, 3] = opacity

    scale = random.uniform(0.1, 0.3)
    width = int(watermark.shape[1] * scale)
    height = int(watermark.shape[0] * scale)
    watermark = cv2.resize(watermark, (width, height))

    x, y = get_random_position(image, watermark.shape[1], watermark.shape[0])

    for i in range(watermark.shape[0]):
        for j in range(watermark.shape[1]):
            if watermark[i, j, 3] > 0:
                image[y + i, x + j] = watermark[i, j]

    return image

# 合并水印（文本或图像水印）
def add_random_watermark(image_path, output_path, watermark_images, opacity=128):
    print(f"Processing {image_path}")  # 添加调试信息
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error loading image: {image_path}")
        return

    # 计算图像亮度并自动调整透明度
    brightness = calculate_image_brightness(image)
    opacity = adjust_opacity_based_on_brightness(brightness)

    # 随机选择文本水印或图像水印
    if random.choice([True, False]):
        watermark_text = get_random_watermark()
        watermarked_image = add_text_watermark_opencv(image, watermark_text, opacity)
    else:
        watermark_image_path = get_random_image_watermark(watermark_images)
        watermarked_image = add_image_watermark_opencv(image, watermark_image_path, opacity)

    # 保存水印图像
    if not cv2.imwrite(output_path, watermarked_image):
        print(f"Failed to save {output_path}")
    else:
        print(f"Saved {output_path}")  # 确认保存成功

# 获取指定文件夹下的所有图片路径
def get_image_files_from_folder(folder_path, extensions=('.jpg', '.jpeg', '.png')):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

# 获取指定文件夹下的所有水印素材图片
def get_watermark_images_from_folder(folder_path, extensions=('.png', '.jpg', '.jpeg')):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

# 批量处理水印，并保证带水印和无水印图像数量一致
def add_random_watermarks_to_batch(image_folder, watermark_folder, output_dir, watermark_probability=0.5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果输出文件夹不存在则创建

    # 获取图片和水印素材
    image_paths = get_image_files_from_folder(image_folder)
    watermark_images = get_watermark_images_from_folder(watermark_folder)

    # 打印加载的文件数量
    print(f"Found {len(image_paths)} images and {len(watermark_images)} watermark images.")

    # 分配水印和无水印图片
    watermarked_images = []
    non_watermarked_images = []

    for image_path in image_paths:
        # 随机决定是否加水印
        if random.random() < watermark_probability:
            output_path = os.path.join(output_dir, f"{os.path.basename(image_path).split('.')[0]}_watermarked.png")
            add_random_watermark(image_path, output_path, watermark_images)  # 加水印
            watermarked_images.append(output_path)
        else:
            output_path = os.path.join(output_dir, f"{os.path.basename(image_path).split('.')[0]}_no_watermark.png")
            cv2.imwrite(output_path, cv2.imread(image_path))  # 保留无水印图像
            non_watermarked_images.append(output_path)

    # 确保水印和无水印图像数量一致
    print(f"Generated {len(watermarked_images)} watermarked images and {len(non_watermarked_images)} non-watermarked images.")

# 示例：批量处理并添加随机水印
image_folder = r"D:\test\UNet\data\image"  # 这里填写存放图片的文件夹路径
watermark_folder = r"D:\test\UNet\data\watermarks"  # 这里填写存放水印素材的文件夹路径
output_dir = r"D:\test\UNet\data\output"  # 输出文件夹

add_random_watermarks_to_batch(image_folder, watermark_folder, output_dir)
