#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.httpserver
from tornado import websocket, web, ioloop
from torndb import Connection

import datetime
import time

import json
import socket
import MySQLdb
from threading import Thread
import hashlib, binascii
import base64

import db_connect as dc

user_handlers = {} #Dict with username as key (return websocket_handler by username)
handler_users = {} #Dict with websocket_handler object as key

def check_connection(request_id, request_type, request_data, ws_heandler):
    print "CheckConnection message" #Debug
    answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
    print "Answer message = ", answer_message
    json_answer_message = json.dumps(answer_message)
    ws_heandler.write_message(json_answer_message)

def log_in(request_id, request_type, request_data, ws_heandler, handler_users, user_handlers):
    print "LogIn message" #Debug
            
    loginClass = json.loads(request_data)
    print loginClass #Debug
    print loginClass['login'] #Debug
    print loginClass['password'] #Debug
    enteredLogin = loginClass['login']
    enteredPassword = loginClass['password']

    #db.execute("SELECT FROM electrolab password WHERE username = login)
    #db.reconnect()
    db = dc.GetConnection()
    dbPasswordStruct = db.get("{}{}{}".format("SELECT password FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
    db.close()    
    print "Password from database", dbPasswordStruct #Debug
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

        #Add user login to dict together with handler
        #logged_users.append(enteredLogin)
        

        db = dc.GetConnection()
        user_info = db.get("{}{}{}".format("SELECT id, first_name, last_name, is_staff, is_superuser FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
        print "user_info = ", user_info
        db.close() 
        
        handler_users.update([(self, user_info['id'])])
        user_handlers.update([(user_info['id'], self)])
        
        #print user_handlers.items()
        #print user_handlers.get("KOS")
        
        #Send to client information about correct login and password
        answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
        print "answer_message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        ws_heandler.write_message(json_answer_message)
        
        #------------------------------------------------------------------------------------------------------
        #Send to client information about UserFullName of current user
        first_name = ""
        last_name = ""

        try:
            first_name = user_info['first_name']
        except KeyError:
            pass

        try:
            last_name = user_info['last_name']
        except KeyError:
            pass
        
        user_full_name = u"{} {}".format(first_name, last_name) 
        answer_message = {'request_id' : request_id, 'request_type' : "UserFullName", 'string_value' : user_full_name}
        print "answer_message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        ws_heandler.write_message(json_answer_message)

        #------------------------------------------------------------------------------------------------------
        #Send to client information about UserRole of current user
        print "is_staff = ", user_info['is_staff']
        print "is_superuser = ", user_info['is_superuser']

        is_staff_flag = user_info['is_staff']
        is_superuser_flag = user_info['is_superuser']

        if((is_staff_flag and is_superuser_flag) or is_superuser_flag):
            user_role_type = 2 #superuser
        elif(is_staff_flag):
            user_role_type = 1 #teacher
        else:
            user_role_type = 0 #student
        
        print "user_role_type = ", user_role_type

        answer_message = {'request_id' : request_id, 'request_type' : "UserRole", 'int_value' : user_role_type}
        print "answer_message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        ws_heandler.write_message(json_answer_message)
        #------------------------------------------------------------------------------------------------------            
        
        #generate answer package with received request_id
        #json_answer = json.dumps()
    else:
        print "Incorrect password"
    
    #self.write_message(json_answer)   
def log_out(request_id, request_type, request_data, ws_heandler, handler_users, user_handlers):
    print "LogOut message"        
    try:
        user_id = handler_users.pop(self)[0]
        del user_handlers[user_id]
        print "User ", username, " was logged out"
        answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
        print "Answer message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        ws_heandler.write_message(json_answer_message)
    except KeyError:
        pass