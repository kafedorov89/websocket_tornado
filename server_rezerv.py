#!/usr/bin/python
# -*- coding: utf-8

import tornado.httpserver
from tornado import websocket, web, ioloop

from torndb import Connection

import json
import socket

import MySQLdb

db = None

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
	

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        print 'new ws connection'
      
    def on_message(self, message):
	    print 'ws message received:  %s' % message
        
	    if(message == "Stand is COMPLETE"):
	    	db.execute("UPDATE `unitygame_electrolab`.`stand_state` SET `complete`='1' WHERE `id`='2';")
        # Reverse Message and send it back
        #print 'sending back message: %s' % message[::-1]
        #self.write_message(message[::-1])
 
    def on_close(self):
        print 'ws connection closed'
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WSHandler),
    (r'/favicon.ico', tornado.web.StaticFileHandler,dict(url='/static/favicon.ico',permanent=False)),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {"path": "plserver"}),
])
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)

    db = Connection('localhost', 'unitygame_electrolab', user='unitygame', password='lstpvzr2!')

    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()