#!/usr/bin/python
# -*-coding=utf-8 -*-

import image
import cv2
import pexif
import urllib


#resp = urllib.urlopen("https://res.shiqichuban.com/v1/image/get/0oM0PYYOqT8Wcbc9EcUjHwfQhFFz7ZX9rAlwj9khYcylwzw_2Ia9NBhTM8zWY0KxVQL0fkAxkqptgbpFCgiGxQ")
#img = pexif.JpegFile.fromFd(resp)
#print(img.exif.primary.Orientation)

files = ["1.png"]
for file in files:
    image.convertURLImage(file,300,0,2,0.5,30)

