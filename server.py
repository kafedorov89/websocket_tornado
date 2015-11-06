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

db = None
handlers = set()
logged_users = []

#@gen.engine
#def f():
#    print 'sleeping'
#    yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)
#    print 'awake!'

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
	

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        print 'new ws connection'
        handlers.add(self)
        #handlers.append(self)

    def check_activate(self):
        print "check_activate"
        #select from db information about activated standtask 

    def add_user(self, user_login):
        print "add_user"

    def on_message(self, message):
	    #Parse request json package
        python_request = json.loads(message)

        #print "python_request['login']: %s" % python_request['login']
        #print "python_request['password']: %s"  % python_request['password']
        #print "python_request['request_id']: %s" % python_request['request_id']
        request_id = python_request[0]
        request_type = python_request[1]
        request_data = python_request[2]

        print 'ws message received:  %s' % python_request
        
        if(request_type == "LogIn"):
            print "LogIn" #Debug
            
            loginClass = json.loads(request_data)
            print loginClass #Debug
            print loginClass['login'] #Debug
            print loginClass['password'] #Debug
            enteredLogin = loginClass['login']
            enteredPassword = loginClass['password']

            #db.execute("SELECT FROM electrolab password WHERE username = login)
            #db.reconnect()
            db = GetConnection()
            dbPasswordStruct = db.get("{}{}{}".format("SELECT password FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
            db.close()    
            print "Password from database : %s " % dbPasswordStruct #Debug
            passwordList = dbPasswordStruct['password'].split('$')
            print passwordList[0] #Debug
            print passwordList[1] #Debug
            print passwordList[2] #Debug
            print passwordList[3] #Debug

            #get salt from db password
            passwordSalt = passwordList[2]
            
            correctPasswordHash = passwordList[3]
            
            #generate hash from entered password
            key = hashlib.pbkdf2_hmac('sha256', enteredPassword.encode('ascii'), passwordSalt.encode('ascii'), 20000)
            
            #binascii.hexlify(dk)
            
            stringKey = base64.b64encode(key).decode('ascii').strip()
            print stringKey #Debug

            #compare with hash from password 
            if(correctPasswordHash == stringKey):
                print "Correct password"
                logged_users.append(enteredLogin)

                #generate answer package with received request_id
                #json_answer = json.dumps()
            else:
                print "Incorrect password"
            
            #self.write_message(json_answer)   

        if(request_type == "LogOut"):
            print "LogOut"

        if(request_type == "CheckComplete"):
	    	db.execute("UPDATE `unitygame_electrolab`.`stand_state` SET `complete`='1' WHERE `id`='2';")
        # Reverse Message and send it back
        #print 'sending back message: %s' % message[::-1]
        #self.write_message(message[::-1])
 
    def on_close(self):
        print 'ws connection closed'
        #handlers.append(self)
        handlers.discard(self)
 
    def check_origin(self, origin):
        return True

def GetConnection():
    return Connection('127.0.0.1', 'electrolab', user='django', password='31415926')

#Function for background calling
def do_something():
    print "background_task"
    for handler in handlers:
        handler.write_message('automatic message')
    #self.write_message(json_answer) 

#Background infinity cycle
@gen.coroutine
def minute_loop():
    while True:
        do_something()
        yield gen.sleep(1)

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WSHandler),
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
    IOLoop.current().spawn_callback(minute_loop)
    IOLoop.instance().start()
    #tornado.ioloop.IOLoop.instance().start()