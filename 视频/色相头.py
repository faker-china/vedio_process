# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 色相头.py
# @Time     : 2024/11/1 上午11:30
# @Software : PyCharm
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("index_camera", help="index of the camera to read from", type=int)
args = parser.parse_args()

capture = cv2.VideoCapture(args.index_camera)
if capture.isOpened()is False:
    print("Error opening the camera")
while capture.isOpened():
    ret, frame = capture.read()

    if ret is True:
        cv2.imshow('Input frame from the camera', frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale input camera', gray_frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    else:
        break
capture.release()
cv2.destroyAllWindows()

