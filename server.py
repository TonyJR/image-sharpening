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
import os
import time

from concurrent.futures import ThreadPoolExecutor

reload(sys)
sys.setdefaultencoding('utf8')

class Executor(ThreadPoolExecutor):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=30)
        return cls._instance



class Handler(tornado.web.RequestHandler):
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
        force = float(self.get_argument("force", default=1))
        smoth = int(self.get_argument("smoth", default=15))
        
        if not image_url:
            result = {}
            result["msg"] = "error"
            self.write(json_encode(result))
        else:
            response = self.converImage(image_url,width,height,force,smoth)
            self.set_header("Content-type", "image/jpeg")
            self.write(response)

    def converImage(self,image_url,width,height,force,smoth):
        bytes = image.convertURLImage(image_url,width,height,4,force,smoth)
        return bytes

    def process(self, image_url):
        print image_url
        return ""

class ImageServer(object):
    
    def __init__(self, port):
        self.port = port
    
    def process(self,server_port):
        app = tornado.web.Application([(r"/image?", Handler)], )
        app.listen(server_port)
        
#        dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#        dir = os.path.dirname(dir)
#        app = tornado.httpserver.HTTPServer(app, ssl_options={
#                                      "certfile": dir+"/cert/test-kv-pub.ures.shiqichuban.com/test-kv-pub.ures.shiqichuban.com.pem",
#                                      "keyfile": dir+"/cert/test-kv-pub.ures.shiqichuban.com/test-kv-pub.ures.shiqichuban.com.key",
#                                      })
#        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    if len(sys.argv)>1:
        server_port = sys.argv[1]
    else:
        server_port = 80

    server = ImageServer(server_port)
    print "begin server"
    server.process(server_port)
