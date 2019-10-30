# -*- coding: utf-8 -*-
import numpy as np
import urllib
import cv2
import time
import os
import random
import pexif
import string


#保存图片
def save_img(img_url):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        
        #下载图片，并保存到文件夹中
        response = urllib.urlopen(img_url)
        firstLine = str(response.readline())
        nowTime = time.time()#生成当前的时间
        randomNum = random.randint(0,100000)#生成随机数n,其中0<=n<=100
        if firstLine.find('PNG') >= 0:
            filename = "/tmp/com.shiqichuban.image-sharpening/"+str(nowTime) + "_" + str(randomNum)+".png"
        else :
            filename = "/tmp/com.shiqichuban.image-sharpening/"+str(nowTime) + "_" + str(randomNum)+".jpg"
        
        
        with open(filename, 'wb') as f:
            f.write(firstLine)
            f.write(response.read())
        return filename
    except IOError as e:
        print '文件操作失败',e
    except Exception as e:
        print '错误 ：',e
        return ""

# URL到图片
def url_to_image(url):
    try:
        
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        resp = urllib.urlopen(url)
        # bytearray将数据转换成（返回）一个新的字节数组
        # asarray 复制数据，将结构化数据转换成ndarray
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        # cv2.imdecode()函数将数据解码成Opencv图像格式
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except:
        print("url下载失败"+url)
        image = cv2.imread("1.jpg")
    finally:
        # return the image
        return image



def convertImage(image,red,green,blue):
    rows,cols,channels=image.shape
    print(rows,cols,channels)
    for i in range(rows):
        for j in range(cols):
            if channels == 4:
                if image[i,j][3] == 0:
                    image[i,j][0] = 0;
                    image[i,j][1] = 0;
                    image[i,j][2] = 0;
                else:
                    image[i,j][0] = blue;
                    image[i,j][1] = green;
                    image[i,j][2] = red;
            else:
                image[i,j][0] = blue;
                image[i,j][1] = green;
                image[i,j][2] = red;
    return image


def convertLocalImage(path,red,green,blue):
    
    
    img = pexif.JpegFile.fromFile(path)
    orientation = img.exif.primary.Orientation
    img.exif.primary.Orientation = [1]
    img.writeFile(path)
    
    
    
    image = cv2.imread(path)
    image = convertImage(image,red,green,blue)
    cv2.imwrite(path,image)
    
    
    img = pexif.JpegFile.fromFile(path)
    img.exif.primary.Orientation = orientation
    img.writeFile(path)
    
    image = cv2.imread(path)
    cv2.imshow(path+"_shape", image)
    
    img_encode = cv2.imencode('.jpg', image)[1]
    
#    return img_encode.tobytes()
    return image

def convertURLToImage(url,red,green,blue):

    if url.find('http') != -1:
        sourcePath = path = save_img(url)
    else:
        path = url
    
    if len(path) <= 0:
        return ""
    
    if path.endswith(('jpg','JPG')):
        tmpPath = convertJPEGImage(path,red,green,blue)
    elif path.endswith(('png','PNG')):
        tmpPath = convertPNGImage(path,red,green,blue)

    image = cv2.imread(tmpPath);

    try:
        os.remove(tmpPath)
    except Exception as e:
        print e
    try:
        os.remove(sourcePath)
    except Exception as e:
        print e

    return image



def convertURLToData(url,red,green,blue):
    if url.find('http') != -1:
        sourcePath = path = save_img(url)
    else:
        path = url
    
    if len(path) <= 0:
        return ""
    
    if path.endswith(('jpg','JPG')):
        tmpPath = convertJPEGImage(path,red,green,blue)
    elif path.endswith(('png','PNG')):
        tmpPath = convertPNGImage(path,red,green,blue)
    
    ##图片转码
    with open(tmpPath, 'r') as f:
        result = f.read()

    try:
        os.remove(tmpPath)
    except Exception as e:
        print e
    try:
        os.remove(sourcePath)
    except Exception as e:
        print e

    return result


def convertPNGImage(path,red,green,blue):
    image = cv2.imread(path,cv2.IMREAD_UNCHANGED)
    #图像处理
    image = convertImage(image,red,green,blue)
    path = path + ".temp.png"
    cv2.imwrite(path,image)

    return path

def convertJPEGImage(path,red,green,blue):
    try:
        img = pexif.JpegFile.fromFile(path)
        orientation = img.exif.primary.Orientation
        img.exif.primary.Orientation = [1]
        img.writeFile(path)
    except Exception as e:
        print "读取orientation失败"
        image = cv2.imread(path)
        #图像处理
        image = convertImage(image,red,green,blue)
        cv2.imwrite(path,image)
        return path

    image = cv2.imread(path)
    #图像处理
    image = convertImage(image,red,green,blue)
    cv2.imwrite(path,image)


    #修改orientation
    try:
        img = pexif.JpegFile.fromFile(path)
        img.exif.primary.Orientation = orientation
        img.writeFile(path)
    except Exception as e:
        print "修改orientation失败"

    return path







