# -*- coding: utf-8 -*-
import numpy as np
import urllib
import cv2
import time

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

#锐化
def sharpening(img,force,smoth):
    
#    kernel = np.array([
#                             [-1,-1,-1,-1,-1],
#                             [-1,2,2,2,-1],
#                             [-1,2,8,2,-1],
#                             [-1,2,2,2,-1],
#                             [-1,-1,-1,-1,-1]])/8.0
#    kernel = np.array([
#                             [1,1,1],
#                             [1,-7,1],
#                             [1,1,1]])
#

    if force == 0:
        overlapping = img
    else:
        kernel = np.array(
                          [[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], np.float32)
        dst = cv2.filter2D(img, -1, kernel=kernel)
        
        if smoth > 0:
            dst = bilateral(dst,6,smoth)
        if force == 1:
            overlapping = dst
        else:
            overlapping = cv2.addWeighted(img, 1-force, dst, force, 0)




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
    image = sharpening(image,force,smoth)
    if scale != 1:
        image = scaleImage(image,width,height)
    return image


def convertLocalImage(path,width=0,height=0,scale=1,force=0,smoth=0):
    if path.find('http') == -1:
        image = cv2.imread(path)
    else :
        image = url_to_image(path)

    image = convertImage(image,width,height,scale,force,smoth)
    cv2.imshow(path+"_shape", image)
    return image



def convertURLImage(url,width=0,height=0,scale=1,force=0,smoth=0):
    start = time.time()
    image = url_to_image(url)
    
    rows,cols,channels=image.shape
    
    t1 = time.time() - start;
    start = time.time()
    image = convertImage(image,width,height,scale,force,smoth)
    img_encode = cv2.imencode('.jpg', image)[1]
    
    t2 = time.time() - start;
    start = time.time()
    
    print("下载"+str(t1)+"锐化"+str(t2)+"\n"+str(cols)+"x"+str(rows)+"_"+str(width)+"x"+str(height)+"\n"+url)
    return img_encode.tobytes()



