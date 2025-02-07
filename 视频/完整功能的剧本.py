# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 完整功能的剧本.py
# @Time     : 2024/10/23 下午6:13
# @Software : PyCharm
import hashlib
import os
import re
import pandas as pd
from langdetect import detect, LangDetectException
import tqdm
import concurrent.futures
import chardet


def get_file_hash(file_path):
    """计算文件的SHA - 1哈希值"""
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def remove_duplicate_and_short_files(directory):
    """删除指定目录中的重复文件（基于文件内容）和字数小于500的txt文档"""
    seen_hashes = {}
    file_paths_to_delete = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as txt_file:
                        content = txt_file.read()
                        if len(content) < 500:
                            file_paths_to_delete.append(file_path)
                            continue
                except Exception as e:
                    print(f"Error reading txt file {file_path}: {e}")
                file_hash = get_file_hash(file_path)
                if file_hash in seen_hashes:
                    file_paths_to_delete.append(file_path)
                else:
                    seen_hashes[file_hash] = file_path

    for file_path in file_paths_to_delete:
        try:
            print(f"Deleting file: {file_path}")
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


def is_chinese(text):
    """判断文本是否为中文，通过正则表达式匹配中文字符"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def has_dialogue(text, language='unknown'):
    """检查文本是否有对话内容，根据语言自动选择对话标志"""
    if language == 'en':
        dialogue_indicators = ['"', "'", ':']
    else:
        dialogue_indicators = ['“', '”', '：']

    dialogue_count = sum([text.count(char) for char in dialogue_indicators])
    return dialogue_count > 0 and (dialogue_count / len(text) > 0.01)


def calculate_dialogue_percentage(text, language='unknown'):
    """计算对话占比，根据语言自动选择对话标志"""
    if language == 'en':
        dialogue_indicators = ['"', "'", ':']
    else:
        dialogue_indicators = ['“', '”', '：']

    dialogue_length = sum([text.count(char) for char in dialogue_indicators])
    return (dialogue_length / len(text)) * 100 if dialogue_length > 0 else 0


def analyze_file(file_path):
    """分析单个文件，返回文件相关信息的字典"""
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            detected_encoding = chardet.detect(raw_data)['encoding']
            if detected_encoding is None:
                print(f"无法确定文件 {file_path} 的编码。")
                return None
            text = raw_data.decode(detected_encoding)
    except Exception as e:
        print(f"读取文件 {file_path} 出错: {e}")
        return None

    try:
        language = detect(text)
    except LangDetectException:
        print(f"检测文件 {file_path} 的语言出错。")
        language = 'unknown'

    file_name = os.path.basename(file_path)
    file_format = file_name.split('.')[-1]
    text_length = len(text)
    has_dialogue_flag = has_dialogue(text, language)
    dialogue_percentage = calculate_dialogue_percentage(text, language)

    return {
        '文件路径': file_path,
        '文件名': file_name,
        '文件格式': file_format,
        '语言类型': language,
        '文本长度': text_length,
        '是否有对话': has_dialogue_flag,
        '对话占比': dialogue_percentage
    }


def analyze_folder(folder_path):
    """分析文件夹中的所有.txt文件，多线程处理，并统计中文和非中文文件数量"""
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

    results = []
    chinese_count = 0
    non_chinese_count = 0
    with tqdm.tqdm(total=len(file_paths), desc="Analyzing files") as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(analyze_file, file_path) for file_path in file_paths]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    if is_chinese(result['文件名']):
                        chinese_count += 1
                    else:
                        non_chinese_count += 1
                pbar.update(1)

    print(f"中文文件数量: {chinese_count}")
    print(f"非中文文件数量: {non_chinese_count}")
    return results


if __name__ == '__main__':
    # 指定文件夹路径
    folder_path = r'D:\文档\1\剧本'
    # 先删除重复和字数小于500的文件
    remove_duplicate_and_short_files(folder_path)
    # 分析文件夹中的所有文件
    folder_info = analyze_folder(folder_path)
    # 将结果保存到Excel文件
    user_directory = os.path.expanduser('~')
    excel_file_path = os.path.join(user_directory, f'{os.path.basename(folder_path)}_analysis.xlsx')
    df = pd.DataFrame(folder_info)
    df.to_excel(excel_file_path, index=False, engine='openpyxl')