#!/usr/bin/python
# -*-coding=utf-8 -*-

import sys
import traceback
from StringIO import StringIO

import requests
import tornado
import tornado.ioloop
import tornado.web
import image
import os

reload(sys)
sys.setdefaultencoding('utf8')


class Handler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Content-MD5, Accept, Accept-Encoding, X-Shiqi-Content-Type, X-Shiqi-Content-Disposition, X-Shiqi-Content-Md5, X-Shiqi-Ctime, X-Shiqi-Filename, X-Shiqi-Position, Refer, User-Agent, Origin, Authorization")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Max-Age","1728000")
    
    def get(self):
        
        
        image_url = self.get_argument("image_url", default="")
        width = int(self.get_argument("width", default=0))
        height = int(self.get_argument("height", default=0))
        force = float(self.get_argument("force", default=0.5))
        smoth = int(self.get_argument("smoth", default=30))

        print image_url
        if not image_url:
            result = {}
            result["msg"] = "error"
            self.write(json_encode(result))
        else:
#            image_url = urllib.urldecode(image_url)
            byte = image.convertURLImage(image_url,width,height,2,force,smoth)
            self.write(byte)
            self.set_header("Content-type", "image/jpeg")


            
    
    def process(self, image_url):
        print image_url
        return ""

class ImageServer(object):
    
    def __init__(self, port):
        self.port = port
    
    def process(self):
        app = tornado.web.Application([(r"/image?", Handler)], )
        app = tornado.httpserver.HTTPServer(app, ssl_options={
                                      "certfile": os.path.join(os.path.abspath("."), "test-kv-pub.ures.shiqichuban.com.crt"),
                                      "keyfile": os.path.join(os.path.abspath("."), "test-kv-pub.ures.shiqichuban.com.key"),
                                      })
        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    server_port = "80"
    server = ImageServer(server_port)
    print "begin server"
    server.process()
