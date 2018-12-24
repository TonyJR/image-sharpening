# -*- coding: utf-8 -*-
import numpy as np
import urllib
import cv2

# URL到图片
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image

#缩放
def scale(img,width,height):
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

    image = cv2.resize(img,(int(width),int(height)),cv2.INTER_LINEAR)
    return image

#锐化
def sharpening(img,alpha,radius):
    kernel = np.array(
                    [[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]], np.float32)
#    kernel = np.array(
#                      [[0,1,0],
#                       [1,-4,1],
#                       [0,1,0]], np.float32)
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
    dst = cv2.filter2D(img, -1, kernel=kernel)
#    dst = bilateral(dst,4,radius)
    overlapping = cv2.addWeighted(img, 1-alpha, dst, alpha, 0)
    

    return overlapping

#    blurred=cv2.GaussianBlur(img,(0,0),1,None,1)
#    lowContrastMask = abs(img - blurred) < threshold
#    sharpened = img*(1+amount) + blurred*(-amount)
#    image=cv2.bitwise_or(sharpened.astype(np.uint8),lowContrastMask.astype(np.uint8))
#    return image

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



def convertImage(image,width,height,force=2,alpha=0.8,radius=50):
    
    rows,cols,channels=image.shape

    image = scale(image,width * force,height * force)
    image = sharpening(image,alpha,radius)
    image = scale(image,width,height)
    return image


def convertLocalImage(path,width,height):
    image = cv2.imread(path)
    cv2.imshow(path, scale(image,width,height).copy())
    image = convertImage(image,width,height)
    cv2.imshow(path+"_shape", image)

    return image

def convertURLImage(url,width,height,force,alpha,radius):
    image = url_to_image(url)
    image = convertImage(image,width,height,force,alpha,radius)
    img_encode = cv2.imencode('.jpg', image)[1]
    return img_encode.tobytes()

## initialize the list of image URLs to download
#url = "https://upload-images.jianshu.io/upload_images/1690384-722e7c32ff6b44b2.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/526"
#
#
#
##image = url_to_image(url)
#
#files = ["1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg"]
#for file in files:
#    image = cv2.imread(file)
#    #image = scale(image,300,300)
#    image = scale(image,800,800)
#
#    cv2.imshow(file, scale(image,400,400))
#    image = bilateral(image,9,5)
#    image = scale(image,400,400)
#    openShapening(file,image,0,0,0.1)
#
#
#cv2.waitKey(0)
