#!/usr/bin/python
# -*- coding: utf-8 -*-

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

        user_name = handler_users[self]
        #session_id = user_sessions[user_name]

        print 'Received message:  %s' % python_request
        
        if(request_type == "UploadAllSchemas"): #Using by admin when upload all schemas to database from local files
            pass
            #get request_data 
            #parse to list with groups (standtask_id, conn_json, rope_json) 
            #upload all groups to main_standtask_data 
        if(request_type == "GetUserRopes"): #Using by teacher when choose student for check his ropes
            pass
            #get user_name from request_data
            #get user_rope_json from main_standtask_user
            #send to self.write_message(json_answer_message)

        if(request_type == "SetComplete"): #Using by student when check complete selected schema
            print "CheckComplete message"
            #Set completed flag to 1 (true) if is_complete flag from request_data is True
            db.execute("UPDATE `electrolab`.`main_standtask_state` SET `complete`='1' WHERE `user_id`=', ';")
 
    def on_close(self):
        print 'Standtask websocket connection was closed'

        answer_message = {'request_id' : "", 'request_type' : "CheckConnection", 'bool_value' : False}
        print "Answer message", answer_message
        json_answer_message = json.dumps(answer_message)
        self.write_message(json_answer_message)
        
        #handlers.append(self)
        handlers.discard(self)
 
    def check_origin(self, origin):
        return True