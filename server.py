#!/usr/bin/python
# -*-coding=utf-8 -*-

import sys
import traceback
import datetime
from StringIO import StringIO

import requests
import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import image
import imageColor
import os
import time

from concurrent.futures import ThreadPoolExecutor

reload(sys)
sys.setdefaultencoding('utf8')

path = "/tmp/com.shiqichuban.image-sharpening"
if not os.path.exists(path):
    os.makedirs(path)

class Executor(ThreadPoolExecutor):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=30)
        return cls._instance



class ImageHandler(tornado.web.RequestHandler):
    executor = Executor()
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Content-MD5, Accept, Accept-Encoding, X-Shiqi-Content-Type, X-Shiqi-Content-Disposition, X-Shiqi-Content-Md5, X-Shiqi-Ctime, X-Shiqi-Filename, X-Shiqi-Position, Refer, User-Agent, Origin, Authorization")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Max-Age","1728000")
        self.set_header("Cache-Control","max-age=2628000")

    @tornado.concurrent.run_on_executor
    def get(self, *args, **kwargs):
        image_url = self.get_argument("image_url", default="")
        width = int(self.get_argument("width", default=0))
        height = int(self.get_argument("height", default=0))
        force = float(self.get_argument("force", default=0))
        smoth = int(self.get_argument("smoth", default=0))
        
        if not image_url:
            result = {}
            result["msg"] = "error"
            self.write(json_encode(result))
        elif image_url.endswith(('png','PNG','gif','GIF')):
            print("png图片重定向"+image_url)
            self.redirect(image_url)
        else:
            response = self.converImage(image_url,width,height,force,smoth)
            self.set_header("Content-type", "image/jpeg")
            self.write(response)

    def converImage(self,image_url,width,height,force,smoth):
        bytes = image.convertURLImage(image_url,width,height,2,force,smoth)
        return bytes

    def process(self, image_url):
        print image_url
        return ""

class ColorHandler(tornado.web.RequestHandler):
    executor = Executor()
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Content-MD5, Accept, Accept-Encoding, X-Shiqi-Content-Type, X-Shiqi-Content-Disposition, X-Shiqi-Content-Md5, X-Shiqi-Ctime, X-Shiqi-Filename, X-Shiqi-Position, Refer, User-Agent, Origin, Authorization")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Max-Age","1728000")
        self.set_header("Cache-Control","max-age=2628000")
    
    @tornado.concurrent.run_on_executor
    def get(self, *args, **kwargs):
        image_url = self.get_argument("image_url", default="")
        color = int(self.get_argument("color", default="0x0"),16)
        red = color >> 16 & 0xff
        green = color  >> 8 & 0xff
        blue = color & 0xff
        
        print color,red,green,blue
        
        if not image_url:
            result = {}
            result["msg"] = "error"
            self.write(json_encode(result))
        else:
            response = self.converImage(image_url,red,green,blue)
            self.set_header("Content-type", "image/x-png")
            self.write(response)

    def converImage(self,image_url,red,green,blue):
        bytes = imageColor.convertURLToData(image_url,red,green,blue)
        return bytes
    
    def process(self, image_url):
        print image_url
        return ""

class ImageServer(object):
    
    def __init__(self, port):
        self.port = port
    
    def process(self,server_port):
        app = tornado.web.Application([(r"/color?", ColorHandler),(r"/image?", ImageHandler)], )
        app.listen(server_port)
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    if len(sys.argv)>1:
        server_port = sys.argv[1]
    else:
        server_port = 80

    server = ImageServer(server_port)
    print "begin server"
    server.process(server_port)
