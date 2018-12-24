#!/usr/bin/python
# -*-coding=utf-8 -*-

import sys
import traceback
from StringIO import StringIO

import requests
import tornado
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode
import image

reload(sys)
sys.setdefaultencoding('utf8')


class Handler(tornado.web.RequestHandler):
    
    def get(self):
        image_url = self.get_argument("image_url", default="")
        width = int(self.get_argument("width", default=1080))
        height = int(self.get_argument("height", default=1080))
        force = int(self.get_argument("force", default=2))
        alpha = int(self.get_argument("alpha", default=0.8))
        radius = int(self.get_argument("radius", default=50))

        print image_url
        if not image_url:
            result = {}
            result["msg"] = "error"
            self.write(json_encode(result))
        else:
            byte = image.convertURLImage(image_url,width,height,force,alpha,radius)
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
        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    server_port = "80"
    server = ImageServer(server_port)
    print "begin server"
    server.process()
