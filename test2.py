#!/usr/bin/python
# -*-coding=utf-8 -*-

import numpy as np
import imageColor
import cv2
import pexif
import urllib



files = ["https://res.shiqichuban.com/v1/image/get/9_6OhitL71cOEIvRTHW_LzIIyeL2JY55x3Gyls-lWAJse9SKe445bMDOxTikFK_bmKlgxFxUXfhNAIiprcab3g"]
for file in files:
    data = imageColor.convertURLToData(file,0,255,0)
#    img = np.asarray(data, dtype="uint8")
#    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imshow("test2",data)
    cv2.waitKey(0)

