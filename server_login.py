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
import MySQLdb
from threading import Thread
import hashlib, binascii
import base64

import db_connect as dc

def check_connection(request_id, request_type, request_data, ws_heandler):
    print "CheckConnection message" #Debug
    answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
    print "Answer message = ", answer_message
    json_answer_message = json.dumps(answer_message)
    ws_heandler.write_message(json_answer_message)

def log_in(request_id, request_type, request_data, ws_heandler):
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
        user_handlers.update([(enteredLogin, self)])

        db = dc.GetConnection()
        user_id = db.get("{}{}{}".format("SELECT id FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))['id']
        print "user_id = ", user_id
        db.close() 
        handler_users.update([(self, [enteredLogin, user_id])])
        
        #print user_handlers.items()
        #print user_handlers.get("KOS")
        
        #Create answer for Callbackfunction in Unity
        answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
        print "answer_message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        ws_heandler.write_message(json_answer_message)
        
        #------------------------------------------------------------------------------------------------------
        #Get information about UserRole of current user
        db = dc.GetConnection()
        dbRoleFlag = db.get("{}{}{}".format("SELECT is_staff, is_superuser FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
        db.close()

        print "is_staff = ", dbRoleFlag['is_staff']
        print "is_superuser = ", dbRoleFlag['is_superuser']

        is_staff_flag = dbRoleFlag['is_staff']
        is_superuser_flag = dbRoleFlag['is_superuser']

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
def log_out(request_id, request_type, request_data, ws_heandler):
    print "LogOut message"        
    try:
        username = handler_users.pop(self)[0]
        del user_handlers[username]
        print "User ", username, " was logged out"
        answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
        print "Answer message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        ws_heandler.write_message(json_answer_message)
    except KeyError:
        pass