#!/usr/bin/python
# -*- coding: utf-8

import tornado.httpserver
from tornado import websocket, web, ioloop

import datetime
import time
from tornado.ioloop import IOLoop
from tornado import gen

import json
import socket

from threading import Thread
import hashlib, binascii
import base64

import db_connect
#import bg_process

from server_stand import StandtaskHandler
from server_stand import check_standtask_activate as csa
#from server_training import TrainingHandler

port_number = 8888;

#handlers = set()
#logged_users = []

#session_id_users = {} #Dict with session_id as key (return username by session_id)

#user_sessions = {} #FIXME. Add methods for add users to dict and remove from dict 

#@gen.engine
#def f():
#    print 'sleeping'
#    yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)
#    print 'awake!'

#class IndexHandler(tornado.web.RequestHandler):
#    def get(self):
#        self.render("index.html")

application = tornado.web.Application([
    #(r'/', IndexHandler),
    #(r'/login', LoginHandler),
    (r'/standtask', StandtaskHandler),
    #(r'/training', TrainingHandler),
    (r'/favicon.ico', tornado.web.StaticFileHandler,dict(url='/static/favicon.ico',permanent=False)),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {"path": "plserver"}),
])

#Background infinity cycle test
@gen.coroutine
def background_loop(delay = 1):
    while True:
        csa()
        yield gen.sleep(delay)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port_number)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Server Started at %s***' % myIP
 
    IOLoop.current().spawn_callback(background_loop) #Stat background_loop
    IOLoop.instance().start() #Start main loop

    #tornado.ioloop.IOLoop.instance().start()

