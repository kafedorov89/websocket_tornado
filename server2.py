#!/usr/bin/python
# -*- coding: utf-8

import tornado.httpserver
from tornado import websocket, web, ioloop
from torndb import Connection

import datetime
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

@gen.coroutine
def auto_loop():
    while True:
        print "auto_loop"
        for handler in handlers:
            handler.write_message('automatic message')

    yield gen.Task(
        IOLoop.current().add_timeout,
        datetime.timedelta(milliseconds=500))

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
            print passwordList[0]
            print passwordList[1]
            print passwordList[2]
            print passwordList[3]

            passwordSalt = passwordList[2]
            correctPasswordHash = passwordList[3]
            ##key = PBKDF2(enteredPassword, passwordSalt).read(32)
            #key = PBKDF2(enteredPassword, passwordSalt, dkLen=32, count=20000, prf=None)
            #key = pbkdf2.encrypt(enteredPassword, salt = passwordSalt.encode('ascii'), rounds = 20000)
            key = hashlib.pbkdf2_hmac('sha256', enteredPassword.encode('ascii'), passwordSalt.encode('ascii'), 20000)
            
            #binascii.hexlify(dk)
            
            stringKey = base64.b64encode(key).decode('ascii').strip()
            print stringKey

            if(correctPasswordHash == stringKey):
                print "Correct password"
                logged_users.append(enteredLogin)
            else:
                print "Incorrect password"
            #get salt from db password
            #generate hash from entered password
            #compare with hash from password 

            #generate anwer package
            ##json_answer = json.dumps()

            #self.write_message()   

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
    auto_loop()
    tornado.ioloop.IOLoop.instance().start()