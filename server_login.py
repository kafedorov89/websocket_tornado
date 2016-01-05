#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.httpserver
from tornado import websocket, web, ioloop
from torndb import Connection
from tornado.websocket import WebSocketHandler, WebSocketClosedError

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
    dbPasswordStruct = db.get("{}{}{}".format("SELECT password, id FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
    db.close()    
    
    try:
        user_handlers[dbPasswordStruct['id']]
        print "User with this ID alredy logged in"
    except KeyError: #If user isn't exit in activated_user list
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
        key1 = hashlib.pbkdf2_hmac('sha256', enteredPassword.encode('ascii'), passwordSalt.encode('ascii'), 24000)
        key2 = hashlib.pbkdf2_hmac('sha256', enteredPassword.encode('ascii'), passwordSalt.encode('ascii'), 20000)
        
        #binascii.hexlify(dk)
        
        stringKey1 = base64.b64encode(key1).decode('ascii').strip()
        stringKey2 = base64.b64encode(key2).decode('ascii').strip()
        print stringKey1 #Debug
        print stringKey2 #Debug

    #compare with hash from password 
        if((correctPasswordHash == stringKey1) or (correctPasswordHash == stringKey2)):
            print "Correct password"

            #Add user login to dict together with handler
            #logged_users.append(enteredLogin)

            db = dc.GetConnection()
            user_info = db.get("{}{}{}".format("SELECT id, first_name, last_name, is_staff, is_superuser FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
            print "user_info = ", user_info
            db.close() 
            
            print "User wasn't activated before"
            handler_users.update([(ws_heandler, user_info['id'])])
            print "handler_users: ", handler_users
            user_handlers.update([(user_info['id'], ws_heandler)])

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
def log_out(request_id, request_type, request_data, ws_heandler):
    print "LogOut message"        
    try:
        #print "handler_users.pop(ws_heandler) = ", handler_users.pop(ws_heandler)
        user_id = handler_users.pop(ws_heandler)

        db = dc.GetConnection()
        username = db.get("{}{}{}".format("SELECT username FROM auth_user WHERE id = \'", user_id, "\' LIMIT 1;")) #REPLACE AFTER FIX
        #username = db.get("{}{}{}".format("SELECT username FROM auth_user WHERE id = \'", user_id, "\' LIMIT 1;")) #REPLACE AFTER FIX
        db.close() 

        print "User ", username, " was logged out"

        del user_handlers[user_id]
        
        answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
        print "Answer message = ", answer_message
        json_answer_message = json.dumps(answer_message)
        
        try:
            ws_heandler.write_message(json_answer_message)
        except WebSocketClosedError:
            print "websocket closed when sending message"

        #print "ws_heandler already was closed"
    except KeyError:
        pass