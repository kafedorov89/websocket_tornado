from tornado import gen
import db_connect

#Function for background looping
def check_standtask_activate():
    print "check_standtask_activate"
    for user_handler in user_handlers:
        pass
        #select from database activate flag of current user and number of current standtask
        #send messages to all users with activated flag in true state
        #user_handler.write_message(json_answer)

#Background infinity cycle test
@gen.coroutine
def background_loop(delay = 1):
    while True:
        check_standtask_activate()
        yield gen.sleep(delay)