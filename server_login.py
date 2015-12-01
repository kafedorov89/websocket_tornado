#!/usr/bin/python
# -*- coding: utf-8 -*-

class LoginHandler(tornado.web.RequestHandler):
    def open(self):
        print 'Training websocket connection was opened'
        #handlers.add(self)
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
                handler_users.update([(self, [enteredLogin, user_id])])
                
                #print user_handlers.items()
                #print user_handlers.get("KOS")
                
                #Create answer for Callbackfunction in Unity
                answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
                print "answer_message = ", answer_message
                json_answer_message = json.dumps(answer_message)
                self.write_message(json_answer_message)
                
                #------------------------------------------------------------------------------------------------------
                #Get information about UserRole of current user
                db = GetConnection()
                dbRoleFlag = db.get("{}{}{}".format("SELECT is_staff, is_superuser FROM auth_user WHERE username = \'", enteredLogin, "\' LIMIT 1;"))
                db.close()

                print "is_staff = ", dbRoleFlag['is_staff']
                print "is_superuser = ", dbRoleFlag['is_superuser']

                is_staff_flag = dbRoleFlag['is_staff']
                is_superuser_flag = dbRoleFlag['is_superuser']

                if((is_staff_flag && is_superuser_flag) || is_superuser_flag):
                    user_role_type = 2 #superuser
                else if(is_staff_flag):
                    user_role_type = 1 #teacher
                else:
                    user_role_type = 0 #student
                
                print "user_role_type = ", user_role_type

                answer_message = {'request_id' : request_id, 'request_type' : "UserRole", 'int_value' : user_role_type}
                print "answer_message = ", answer_message
                json_answer_message = json.dumps(answer_message)
                self.write_message(json_answer_message)
                #------------------------------------------------------------------------------------------------------            
                
                #generate answer package with received request_id
                #json_answer = json.dumps()
            else:
                print "Incorrect password"
            
            #self.write_message(json_answer)   

        if(request_type == "LogOut"):
            print "LogOut message"
            
            try:
                username = handler_users.pop(self)[0]
                del user_handlers[username]
                print "User ", username, " was logged out"
                answer_message = {'request_id' : request_id, 'request_type' : request_type, 'bool_value' : True}
                print "Answer message = ", answer_message
                json_answer_message = json.dumps(answer_message)
                self.write_message(json_answer_message)
            except KeyError:
                pass

    def on_close(self):
        print 'Training websocket connection was closed'
        #handlers.append(self)
        handlers.discard(self)
 
    def check_origin(self, origin):
        return True
