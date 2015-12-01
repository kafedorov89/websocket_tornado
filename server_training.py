#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        
        if(request_type == "GetSessions"):
            print "GetSessions message" #Debug
            #Send list with all created sessions

        if(request_type == "JoinToSession"):
            print "JoinToSession message" #Debug
            #Add user to one of created sessions

        if(request_type == "CreateSession"):
            print "CreateSession message" #Debug
            #Create new session id and add user to new session

        if(request_type == "Viss"):
            print "Viss message" #Debug
            #Send Visualizations id to all connected users in current session

        if(request_type == "Params"):
            print "Params message" #Debug
            #Send Params id with values to all connected users in current session

        if(request_type == "Event"):
            print "Event message" #Debug
            #Write event to database
    
    def on_close(self):
        print 'Training websocket connection was closed'
        #handlers.append(self)
        handlers.discard(self)
 
    def check_origin(self, origin):
        return True