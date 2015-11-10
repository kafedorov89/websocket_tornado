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
#logged_users = []
user_handlers = {}
handler_users = {}

#@gen.engine
#def f():
#    print 'sleeping'
#    yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)
#    print 'awake!'

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
	
class TrainingHandler(websocket.WebSocketHandler):
    def open(self):
        print 'Training websocket connection was opened'
        handlers.add(self)
        #handlers.append(self)

    def on_message(self, message):
		print 'Received message from Training websocket connection'

	    #Parse request json package
        python_request = json.loads(message)

        #print "python_request['login']: %s" % python_request['login']
        #print "python_request['password']: %s"  % python_request['password']
        #print "python_request['request_id']: %s" % python_request['request_id']
        request_id = python_request[0]
        request_type = python_request[1]
        request_data = python_request[2]

        print 'Received message:  %s' % python_request
        
		if(request_type == "Viss"):
			print "Viss message" #Debug
			#Send Visualizations id to all connected users in current training

		if(request_type == "Params"):
			print "Params message" #Debug
			#Send Params id with values to all connected users in current training

		if(request_type == "Event"):
			print "Event message" #Debug
			#Write event to database
    
    def on_close(self):
        print 'Training websocket connection was closed'
        #handlers.append(self)
        handlers.discard(self)
 
    def check_origin(self, origin):
        return True


class StandtaskHandler(websocket.WebSocketHandler):
    def open(self):
        print 'Standtask websocket connection was opened'
        handlers.add(self)
        #handlers.append(self)

    def on_message(self, message):
    	print 'Received message from Standtask websocket connection'
	    #Parse request json package
        python_request = json.loads(message)

        #print "python_request['login']: %s" % python_request['login']
        #print "python_request['password']: %s"  % python_request['password']
        #print "python_request['request_id']: %s" % python_request['request_id']
        request_id = python_request[0]
        request_type = python_request[1]
        request_data = python_request[2]

        print 'Received message:  %s' % python_request
        
		if(request_type == "CheckConnection"):
			print "CheckConnection message" #Debug
			answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
            print "Answer message = ", answer_message
            json_answer_message = json.dumps(answer_message)
            self.write_message(json_answer_message)

        if(request_type == "LogIn"):
            print "LogIn message" #Debug
            
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

                #Add user login to dict with together with handler
                #logged_users.append(enteredLogin)
                user_handlers.update([(enteredLogin, self)])
                handler_users.update([(self, enteredLogin)])
                
                print user_handlers.items()
                print user_handlers.get("KOS")
                
                answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
                print "answer_message = ", answer_message
                json_answer_message = json.dumps(answer_message)
                self.write_message(json_answer_message)
                #generate answer package with received request_id
                #json_answer = json.dumps()
            else:
                print "Incorrect password"
            
            #self.write_message(json_answer)   

        if(request_type == "LogOut"):
            print "LogOut message"
            
            try:
                user_name = handler_users.pop(self)
                del user_handlers[user_name]
                print "User ", user_name, " was logged out"
                answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
                print "Answer message = ", answer_message
                json_answer_message = json.dumps(answer_message)
                self.write_message(json_answer_message)
            except KeyError:
                pass
           
        if(request_type == "CheckComplete"):
        	print "CheckComplete message"
	    	db.execute("UPDATE `unitygame_electrolab`.`stand_state` SET `complete`='1' WHERE `id`='2';")
	        # Reverse Message and send it back
	        #print 'sending back message: %s' % message[::-1]
	        #self.write_message(message[::-1])
 
    def on_close(self):
        print 'Standtask websocket connection was closed'
        #handlers.append(self)
        handlers.discard(self)
 
    def check_origin(self, origin):
        return True

def GetConnection():
    return Connection('127.0.0.1', 'electrolab', user='django', password='31415926')

#Function for background looping
def check_standtask_activate():
    print "check_standtask_activate"
    for user_handler in user_handlers:
    	#select from database activate state of current user and number of current standtask
 		#send messages to all users with activated flag in true state
    	#self.write_message(json_answer) 

#Background infinity cycle test
@gen.coroutine
def background_loop(delay = 1):
    while True:
        check_standtask_activate()
        yield gen.sleep(delay)

application = tornado.web.Application([
    (r'/', IndexHandler),
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
    IOLoop.current().spawn_callback(background_loop) #Stat background_loop
    IOLoop.instance().start() #Start main loop
    #tornado.ioloop.IOLoop.instance().start()