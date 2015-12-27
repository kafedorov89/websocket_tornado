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

activated_user = []

#Function for background looping
def check_standtask_activate():
    print "check_standtask_activate"
    
    db = dc.GetConnection()
    activate_list = db.query("SELECT id, user_id, standtask_id FROM main_standtask_state WHERE activate = 1") #REPLACE AFTER FIX
    #activate_list = db.query("SELECT id, user_id_id, standtask_id_id FROM main_standtask_state WHERE activate = 1") #REPLACE AFTER FIX

    user_id_list = []
    standtask_id_list = []

    print "len(activate_list) = ", len(activate_list) 

    for active_standtask in activate_list:
        try:
            activated_user.index(active_standtask['user_id'])
        except ValueError: #If user isn't exit in activated_user list
            try:
            #Get ws_handler for activate user_id
                user_handler = lg.user_handlers[active_standtask['user_id']] #REPLACE AFTER FIX
                #print "---handler_users: ", lg.handler_users

                #Get line in table main_standtask_state
                activate_standtask_id = active_standtask['id'] 
                
                #Get standtask_id for activate
                standtask_id = active_standtask['standtask_id'] #REPLACE AFTER FIX
                #standtask_id = active_standtask['standtask_id_id'] #REPLACE AFTER FIX

                #Get activated standtask conn_json
                standtask_data = db.get("{}{}{}".format("SELECT conn_json, standtask_name FROM main_standtask WHERE id = \'", standtask_id, "\';"))

                #Send activate message to user. This message contain information about correct connections for activated standtask
                answer_message = {'request_id' : '', 'request_type' : 'ActivateStandtask', 'int_list' : [activate_standtask_id, standtask_id], 'string_value' : standtask_data['conn_json']}
                
                #print "answer_message = ", answer_message
                json_answer_message = json.dumps(answer_message)
                user_handler.write_message(json_answer_message)

                print "Activate, standtask №", standtask_id, ", user_id = ", active_standtask['user_id'] #REPLACE AFTER FIX
                #print "Activate, standtask №", standtask_id, ", user_id = ", active_standtask['user_id_id'] #REPLACE AFTER FIX

                #Add new user to activated_user list for stop activation again and again
                activated_user.append(active_standtask['user_id']);
            except KeyError:
                print "User with activated standtask not logged in to 3D application, yet"    
    db.close()


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

        #print 'Received message:  %s' % python_request

        if(request_type == "CheckConnection"):
            lg.check_connection(request_id, request_type, request_data, self)

        if(request_type == "LogIn"):
            lg.log_in(request_id, request_type, request_data, self)

        if(request_type == "LogOut"):
            #Remove user_id from activated_user list
            try:
            #print "LogOut handler_users: ", lg.handler_users
                activated_user.remove(lg.handler_users[self]);
            except KeyError:
                print "KeyError: This user_id isn't exist in activated_user list"
            except ValueError:
                print "ValueError: This user_id isn't exist in activated_user list"

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
            #user_id, 
            
            db = dc.GetConnection()
            activate_list = db.query("SELECT id, user_id, standtask_id FROM main_standtask_state WHERE activate = 1")
            
            active_standtask_id_list = []
            standtask_name_list = []

            for active_standtask in activate_list:
                print "active_standtask = ", active_standtask
                standtask_name = db.get("{}{}{}".format("SELECT standtask_name FROM main_standtask_data WHERE standtask_id = \'", active_standtask['standtask_id'], "\';"))
                print "standtask_name = ", standtask_name 
                
                user_fullname = db.get("{}{}{}".format("SELECT first_name, last_name FROM auth_user WHERE id = \'", active_standtask['user_id'], "\';"))
                print "user_fullname = ", user_fullname

                active_standtask_id_list.append(active_standtask['id'])
                standtask_name_list.append(u"Лабораторная работа №{} Студент:{} {}".format(standtask_name['standtask_name'], user_fullname['first_name'], user_fullname['last_name']))
            
            db.close()

            print "active_standtask_id_list = ", active_standtask_id_list
            print "standtask_name_list = ", standtask_name_list

            answer_message = {'request_id' : request_id, 'request_type' : request_type, 'int_list' : active_standtask_id_list, 'string_list' : standtask_name_list}
            print "Answer message = ", answer_message
            json_answer_message = json.dumps(answer_message)
            self.write_message(json_answer_message)

        if(request_type == "GetStudentStandtask"): #Using by teacher when choose student for check his ropes
            active_standtask_id = json.loads(request_data)
            print "active_standtask_info = ", active_standtask_id

            db = dc.GetConnection()
            active_standtask_state = db.get("{}{}{}".format("SELECT user_id, standtask_id, user_rope_json FROM main_standtask_state WHERE id = \'", active_standtask_id, "\';"))
            
            user_name = db.get("{}{}{}".format("SELECT first_name, last_name FROM auth_user WHERE id = \'", active_standtask_state['user_id'], "\';"))
            user_full_name = u"{} {}".format(user_name['first_name'], user_name['last_name'])

            active_standtask_data = db.get("{}{}{}".format("SELECT conn_json, standtask_name FROM main_standtask WHERE id = \'", active_standtask_state['standtask_id'], "\';"))
            print "active_standtask_state = ", active_standtask_state 
            print "active_standtask_data = ", active_standtask_data 

            answer_message = {'request_id' : request_id, \
                'request_type' : request_type, \
                'string_list' : [active_standtask_state['user_rope_json'], \
                                active_standtask_data['conn_json'], \
                                user_full_name, \
                                active_standtask_data['standtask_name']],\
                'int_value' : active_standtask_state['standtask_id']}
            #pass
            #get active_standtask_id from request_data
            #get user_rope_json and full_username from main_standtask_state and auth_user
            json_answer_message = json.dumps(answer_message)
            self.write_message(json_answer_message)

        if(request_type == "GetSchema"): #Using by admin when checking all schemas uploading
            standtask_id = json.loads(request_data)
            db = dc.GetConnection()
            standtask = db.get("{}{}{}".format("SELECT conn_json, rope_json FROM main_standtask_data WHERE standtask_id = \'", standtask_id, "\';"))

            conn_json = standtask['conn_json']
            rope_json = standtask['rope_json']

            answer_message = {'request_id' : request_id, \
                'request_type' : request_type, \
                'string_list' : [conn_json, rope_json]}
            #pass
            #get active_standtask_id from request_data
            #get user_rope_json and full_username from main_standtask_state and auth_user
            json_answer_message = json.dumps(answer_message)
            self.write_message(json_answer_message)

        if(request_type == "UploadAllSchemas"): #Using by admin when upload all schemas to database from local files
            standtask_data = json.loads(request_data) #Unpask all standtasks from one package
            
            db = dc.GetConnection()
            #Remove all standtasks from database
            

            #db.execute("SET SQL_SAFE_UPDATES = 0; DELETE FROM main_standtask_data; ALTER TABLE main_standtask_data AUTO_INCREMENT = 1; SET SQL_SAFE_UPDATES = 1;")

            for standtask_json in standtask_data:
                
                standtask = json.loads(standtask_json) #Unpack one standtask from one file

                standtask_id = standtask['standtask_id']
                standtask_name = ''#standtask['standtask_name']
                #conn_json = json.dumps(standtask['conn_json'])
                #rope_json = json.dumps(standtask['rope_json'])
                conn_json = standtask['conn_json']
                rope_json = standtask['rope_json']
                #conn_json = "{}".format(json.loads(standtask['conn_json']))
                #rope_json = "{}".format(json.loads(standtask['rope_json']))

                print "\n\n\n", "conn_json = ", conn_json, "\n\n\n"
                print "rope_json = ", rope_json, "\n\n\n"

                #db.execute("INSERT INTO `electrolab`.`main_standtask_data` ('standtask_id','standtask_name','conn_json','rope_json',) \
                #VALUES(\'",standtask_id,"\', \'",standtask_name,"\', \'",conn_json,"\', \'",rope_json,"\')");
                
                sql_reeequest = "INSERT INTO `electrolab`.`main_standtask` (`id`,`standtask_name`,`conn_json`,`rope_json`) \
                VALUES({0}, \'\'\'{1}\'\'\', \'\'\'{2}\'\'\', \'\'\'{3}\'\'\') \
                ON DUPLICATE KEY UPDATE `conn_json` = \'\'\'{2}\'\'\', `rope_json` = \'\'\'{3}\'\'\';".format(standtask_id, standtask_name, conn_json, rope_json)

                #sql_reeequest = "INSERT INTO `electrolab`.`main_standtask` (`id`,`standtask_name`,`conn_json`,`rope_json`) \
                #VALUES({0}, \'\'\'{1}\'\'\', {2}, {3}) \
                #ON DUPLICATE KEY UPDATE `conn_json` = {2}, `rope_json` = {3};".format(standtask_id, standtask_name, conn_json, rope_json)

                print "\n\n\n", sql_reeequest, "\n\n\n"

                #sql_reeequest = "INSERT INTO `electrolab`.`main_standtask_data` ('standtask_id','standtask_name','conn_json','rope_json',) \
                #VALUES(\'",standtask_id,"\', \'",standtask_name,"\', \'",conn_json,"\', \'",rope_json,"\') \
                #ON DUPLICATE KEY UPDATE `conn_json` = \'",conn_json,"\', `rope_json` = \'",rope_json,"\';".format(standtask_id, standtask_name, conn_json, rope_json)

                db.execute(sql_reeequest)
                #ON DUPLICATE KEY UPDATE `conn_json` = \'", str(json.loads(conn_json)[0]) ,"\', `rope_json` = \'", str(json.loads(rope_json)[0]) ,"\';")

            #db.execute("{}{}".format("INSERT INTO `electrolab`.`main_standtask_data` SET `user_rope_json`=\'", user_rope_json,"\',"\';"))
            db.close()
            #get request_data with standtask_id, conn_json, rope_json
            #parse to list with groups (standtask_id, conn_json, rope_json) for each standtask 
            #upload all groups to main_standtask_data, each to one row

        if(request_type == "UploadStudentRopes"): #Using by student, when new rope was fixed in some socket and need update information on server for teacher
            user_rope = json.loads(request_data)
            user_rope_json = user_rope['user_rope_json']
            active_standtask_id = user_rope['active_standtask_id']

            db = dc.GetConnection()
            db.execute("{}{}{}{}{}".format("UPDATE `electrolab`.`main_standtask_state` SET `user_rope_json`=\'", user_rope_json,"\' WHERE `id`=\'", active_standtask_id,"\';"))
            db.close()
            #get request_data with standtask_id, conn_json, rope_json
            #parse to list with groups (standtask_id, conn_json, rope_json) for each standtask 
            #upload all groups to main_standtask_data, each to one row 

        if(request_type == "SetStandtaskComplete"): #Using by student when check complete selected schema
            activated_user.remove(active_standtask['user_id_id']); #FIXME. Need to add in request data, information about user_id, who completed this standtask

            active_standtask_id = json.loads(request_data)

            print "CheckComplete message"
            #Set completed flag to 1 (true) if is_complete flag from request_data is True
            db = dc.GetConnection()
            db.execute("UPDATE `electrolab`.`main_standtask_state` SET `complete`='1', 'activate'='0' WHERE `active_standtask_id`=\'",active_standtask_id,"\';")
            db.close()


    def on_close(self):
        print 'Standtask websocket connection was closed'

        print "handler_users: ", lg.handler_users
        print "activated_user: ", activated_user
        print "lg.handler_users[self]: ", lg.handler_users[self]
 
        #Remove user_id from activated_user list
        try:
            activated_user.remove(lg.handler_users[self]);
        except ValueError:
            print "This user_id isn't exist in activated_user list"
        
        lg.log_out("", "LogOut", "", self)

        #FIXME. Send to main_standtask_state table 'error' = '1' and 'activate' = '0' if line with active_standtask_id have 'activate' = '1'

        #answer_message = {'request_id' : "", 'request_type' : "CheckConnection", 'bool_value' : False}
        #print "Answer message", answer_message
        #json_answer_message = json.dumps(answer_message)
        #self.write_message(json_answer_message)
        
        #handlers.append(self)
        #handlers.discard(self)
 
    def check_origin(self, origin):
        return True