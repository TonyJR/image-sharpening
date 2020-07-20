#!/usr/bin/python
# -*-coding=utf-8 -*-

import image
import cv2
import pexif
import urllib



files = ["test.png"]
for file in files:
    image.convertURLImage(file,20,0,2,0.5,30)

