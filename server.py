#!/usr/bin/python
# -*- coding: utf-8

import tornado.httpserver
from tornado import websocket, web, ioloop
from torndb import Connection

import datetime
import time
from tornado.ioloop import IOLoop
from tornado import gen

import json
import socket
import MySQLdb
from threading import Thread
import hashlib, binascii
import base64

#Import class for server
from server_training import LoginHandler
from server_stand import StandtaskHandler
from server_login import LoginHandler

db = None
handlers = set()
#logged_users = []

user_handlers = {} #Dict with username as key
handler_users = {} #Dict with websocket_handler object as key

#user_sessions = {} #FIXME. Add methods for add users to dict and remove from dict 

#@gen.engine
#def f():
#    print 'sleeping'
#    yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)
#    print 'awake!'

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def GetConnection():
    return Connection('127.0.0.1', 'electrolab', user='django', password='31415926')

#Function for background looping
def check_standtask_activate():
    print "check_standtask_activate"
    for user_handler in user_handlers:
        pass
        #select from database activate flag of current user and number of current standtask
        #send messages to all users with activated flag in true state
        #user_handler.write_message(json_answer)

#Background infinity cycle test
@gen.coroutine
def background_loop(delay = 1):
    while True:
        check_standtask_activate()
        yield gen.sleep(delay)

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/standtask', StandtaskHandler),
    (r'/training', TrainingHandler),
    (r'/favicon.ico', tornado.web.StaticFileHandler,dict(url='/static/favicon.ico',permanent=False)),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {"path": "plserver"}),
])
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Server Started at %s***' % myIP
    #auto_loop()
    #IOLoop.instance().add_callback(f)
    
    #IOLoop.current().spawn_callback(background_loop) #Stat background_loop
    IOLoop.instance().start() #Start main loop
    
    #tornado.ioloop.IOLoop.instance().start()