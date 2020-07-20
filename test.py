#!/usr/bin/python
# -*-coding=utf-8 -*-

import image
import cv2
import pexif
import urllib



files = ["http://img2020.cnblogs.com/blog/2016690/202007/2016690-20200717105942214-957138008.png"]
for file in files:
    image.convertURLImage(file,300,0,2,0.5,30)

