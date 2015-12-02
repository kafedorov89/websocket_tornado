#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.httpserver
from tornado import websocket, web, ioloop
from torndb import Connection

import datetime
import time
from tornado.ioloop import IOLoop
from tornado import gen

import json
import socket
#import MySQLdb
from threading import Thread
import hashlib, binascii
import base64

import db_connect as dc
import server_login as lg

user_handlers = {} #Dict with username as key (return websocket_handler by username)
handler_users = {} #Dict with websocket_handler object as key

class StandtaskHandler(websocket.WebSocketHandler):
    def open(self):
        print 'Standtask websocket connection was opened'
        #handlers.add(self)
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

        #session_id = user_sessions[user_name]

        print 'Received message:  %s' % python_request

        if(request_type == "CheckConnection"):
            lg.check_connection(request_id, request_type, request_data, self)

        if(request_type == "LogIn"):
            lg.log_in(request_id, request_type, request_data, self)

        if(request_type == "LogOut"):
            lg.log_out(request_id, request_type, request_data, self)



        #username = handler_users[self]
        if(request_type == "GetStudentStandtaskList"): #Using by teacher when choose student for check his ropes
            #loginClass = json.loads(request_data)
            #print loginClass #Debug
            #print loginClass['login'] #Debug
            #print loginClass['password'] #Debug
            
            #enteredLogin = loginClass['login']
            #enteredPassword = loginClass['password']
            #get list with active user from main_standtask_state
            user_id, 
            
            db = dc.GetConnection()
            user_id_list = db.get("SELECT user_id, standtask_id FROM main_standtask_state WHERE activate = 1")
            #user_info_list = username, first_name, last_name, standtask_id
            db.close()

            print "user_id list = ", user_id_list

            ##send to self.write_message(json_answer_message)
            #print "List with active users ", username, " was logged out"
            #answer_message = {'request_id' : request_id, 'request_type' : request_type, 'string_list' : ['username1', 'username2', 'username3']}
            #print "Answer message = ", answer_message
            #json_answer_message = json.dumps(answer_message)
            #self.write_message(json_answer_message)

        if(request_type == "GetStudentStandtask"): #Using by teacher when choose student for check his ropes
            pass
            #get user_name from request_data
            #get user_rope_json and full_username from main_standtask_user
            #send to self.write_message(json_answer_message)

        if(request_type == "UploadAllSchemas"): #Using by admin when upload all schemas to database from local files
            pass
            #get request_data with standtask_id, conn_json, rope_json
            #parse to list with groups (standtask_id, conn_json, rope_json) for each standtask 
            #upload all groups to main_standtask_data, each to one row

        if(request_type == "UploadAllSchemas"): #Using by admin when upload all schemas to database from local files
            pass
            #get request_data with standtask_id, conn_json, rope_json
            #parse to list with groups (standtask_id, conn_json, rope_json) for each standtask 
            #upload all groups to main_standtask_data, each to one row 

        if(request_type == "SetStandtaskComplete"): #Using by student when check complete selected schema
            print "CheckComplete message"
            #Set completed flag to 1 (true) if is_complete flag from request_data is True
            db = dc.GetConnection()
            db.execute("UPDATE `electrolab`.`main_standtask_state` SET `complete`='1' WHERE `user_id`=', ';")
            db.close()


    def on_close(self):
        print 'Standtask websocket connection was closed'

        #answer_message = {'request_id' : "", 'request_type' : "CheckConnection", 'bool_value' : False}
        #print "Answer message", answer_message
        #json_answer_message = json.dumps(answer_message)
        #self.write_message(json_answer_message)
        
        #handlers.append(self)
        #handlers.discard(self)
 
    def check_origin(self, origin):
        return True