# -*- coding: utf-8 -*-
import numpy as np
import urllib
import cv2
import time
import os
import random
import pexif


#保存图片
def save_img(img_url):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        
        #下载图片，并保存到文件夹中
        response = urllib.urlopen(img_url)
        
        
        nowTime = time.time()#生成当前的时间
        randomNum = random.randint(0,100000)#生成随机数n,其中0<=n<=100
        filename = "/tmp/com.shiqichuban.image-sharpening/"+str(nowTime) + "_" + str(randomNum)+".jpg"
        
        with open(filename, 'wb') as f:
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

#缩放
def scaleImage(img,width,height):
    rows,cols,channels=img.shape
    ratio1 = float(cols) / float(rows)
    if width == 0:
        if height == 0:
            return img
        else:
            width = height * ratio1
    elif height == 0:
        height = width / ratio1
    else :
        ratio2 = float(width) / float(height)
        if ratio1 > ratio2:
            height = width / ratio1
        else :
            width = height * ratio1

#    if width >= rows:
#        return img
    image = cv2.resize(img,(int(width),int(height)),cv2.INTER_LINEAR)
    return image

#高反差保留
def sobel(img):
    x=cv2.Sobel(img,cv2.CV_16S,1,0)
    y=cv2.Sobel(img,cv2.CV_16S,0,1)
    absx=cv2.convertScaleAbs(x)
    absy=cv2.convertScaleAbs(y)
    dist=cv2.addWeighted(absx,0.5,absy,0.5,0)
    force = 0.1
    dist = cv2.addWeighted(img, 1, dist, force, 0)
    return dist

#锐化
def sharpening(img,force,smoth):
#    kernel = np.array([
#                             [1,1,1],
#                             [1,-7,1],
#                             [1,1,1]])
#

    if force == 0:
        overlapping = img
    else:
#        kernel = np.array(
#                          [[0, -1, 0],
#                           [-1, 5, -1],
#                           [0, -1, 0]], np.float32)
#        dst = cv2.filter2D(dst, -1, kernel=kernel)
        dst = img#sobel(img)
        kernel = np.array([
                           [-1,-1,-1,-1,-1],
                           [-1,2,2,2,-1],
                           [-1,2,8,2,-1],
                           [-1,2,2,2,-1],
                           [-1,-1,-1,-1,-1]])/8.0
        dst = cv2.filter2D(dst, -1, kernel=kernel)

        
        if force == 1:
            overlapping = dst
        else:
            overlapping = cv2.addWeighted(img, 1-force, dst, force, 0)
        if smoth > 0:
            overlapping = bilateral(overlapping,6,smoth)



    return overlapping


#高斯模糊
def gaussian(img):
    blur=cv2.GaussianBlur(img,(0,0),3)
    image=cv2.addWeighted(img,1.5,blur,-0.5,0)
    return image



#磨皮
def bilateral(img,times,radius):
    image=cv2.bilateralFilter(img,times,radius,radius)
    return image




def get_light(img):
    return np.average(img[:,:])



def turn_light(img, scale, offset):
    
    rows,cols,channels=img.shape
    a=scale
    b=offset
#    for c in range(3):
#    dst = img[:,:][:] * a
    dst = img.copy()
    for i in range(rows):
        for j in range(cols):
            for c in range(3):
                color=img[i,j][c] * a + b
                if color>255:
                    dst[i,j][c]=255
                elif color<0:
                    dst[i,j][c]=0
    return dst



def convertImage(image,width,height,scale,force,smoth):
    
    rows,cols,channels=image.shape

    image = scaleImage(image,width * scale,height * scale)
    image = sharpening(image,force,smoth/scale)
    if scale != 1:
        image = scaleImage(image,width,height)
    image = sobel(image)
    return image


def convertLocalImage(path,width=0,height=0,scale=1,force=0,smoth=0):
    
    
    img = pexif.JpegFile.fromFile(path)
    orientation = img.exif.primary.Orientation
    img.exif.primary.Orientation = [1]
    img.writeFile(path)



    image = cv2.imread(path)
    image = convertImage(image,width,height,scale,force,smoth)
    cv2.imwrite(path,image)


    img = pexif.JpegFile.fromFile(path)
    img.exif.primary.Orientation = orientation
    img.writeFile(path)

    image = cv2.imread(path)
    cv2.imshow(path+"_shape", image)

    img_encode = cv2.imencode('.jpg', image)[1]

    return img_encode.tobytes()



def convertURLImage(url,width=0,height=0,scale=1,force=0,smoth=0):
    start = time.time()
    
    if url.find('http') != -1:
        path = save_img(url)
    else:
        path = url

    if len(path) <= 0:
        return ""


    img = pexif.JpegFile.fromFile(path)

    try:
        orientation = img.exif.primary.Orientation
        img.exif.primary.Orientation = [1]
        img.writeFile(path)
    except Exception as e:
        print "读取orientation失败"


    
    image = cv2.imread(path)
    rows,cols,channels=image.shape

    t1 = time.time() - start;
    start = time.time()

#锐化图片
    image = convertImage(image,width,height,scale,force,smoth)
    cv2.imwrite(path,image)
    t2 = time.time() - start;
    start = time.time()


#修改orientation
    try:
        img = pexif.JpegFile.fromFile(path)
        img.exif.primary.Orientation = orientation
        img.writeFile(path)
    except Exception as e:
        print "修改orientation失败"

#图片转码
    image = cv2.imread(path)
    img_encode = cv2.imencode('.jpg', image)[1]


    print("下载"+str(t1)+"锐化"+str(t2)+"\n"+str(cols)+"x"+str(rows)+"_"+str(width)+"x"+str(height)+"\n"+url)
    if url.find('http') != -1:
        os.remove(path)

    return img_encode.tobytes()



    

    




