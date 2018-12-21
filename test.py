#!/usr/bin/python
# -*-coding=utf-8 -*-

import image
import cv2


files = ["7.jpg","8.jpg"]
for file in files:
    image.convertLocalImage(file,800,800)

cv2.waitKey(0)
