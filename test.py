#!/usr/bin/python
# -*-coding=utf-8 -*-

import image
import cv2


files = ["https://img1.360buyimg.com/pop/jfs/t1/25083/31/1438/41872/5c120ac3Ea1bf3da5/a66357ea96a6917b.jpg","1.jpg","7.jpg","8.jpg"]
for file in files:
    image.convertLocalImage(file,300,0,2,0.5,30)

cv2.waitKey(0)
