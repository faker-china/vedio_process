# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : imagetest.py
# @Time     : 2025-03-31 16:10
# @Software : PyCharm
import cv2
image=cv2.imread("3_1.jpg")
print("获取彩色图像的属性：")
print("shape=",image.shape)
print("size=",image.size)
print("dtype=",image.dtype)
image_gray=cv2.imread("3_1.jpg",0)
print("获取灰度图像的属性：")
print("shape=",image_gray.shape)
print("size=",image_gray.size)
print("dtype=",image_gray.dtype)
cv2.imshow("dog",image)
cv2.imshow("dog_gray",image_gray)
cv2.waitKey()
cv2.destroyAllWindows()