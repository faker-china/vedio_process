# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : nltk数据下载.py
# @Time     : 2024/10/24 上午9:08
# @Software : PyCharm
import nltk

nltk.data.path.append('D:\\nltk_data')
nltk.download('punkt', download_dir='D:\\nltk_data')
nltk.download('stopwords', download_dir='D:\\nltk_data')