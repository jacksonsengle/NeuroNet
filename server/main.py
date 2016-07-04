#!/usr/bin/env python
"""
    main.py
    =======

    Main tornado server for NeuroNet.

    :created: 2016-07-03 23:35:23 -0700
    :copyright: (c) 2016, Lambda Labs, Inc.
    :license: All Rights Reserved.
"""
import datetime
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web



class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []
    client_info = {}

    def check_origin(self, origin):
        return True

    def open(self):
        print('new connection')
        self.write_message("Hello World")
        WSHandler.clients.append(self)
        WSHandler.client_info[hash(self)] = {}

    def on_message(self, message):
        if 'name: ' in message:
            name = message.split('name: ')[1]
            WSHandler.client_info[hash(self)]['name'] = name
        else:
            WSHandler.client_info[hash(self)].get('name', 'Somebody')
            WSHandler.broadcast('{}: {}'.format(client_name, message))

    def on_close(self):
        print('connection closed')
        WSHandler.clients.remove(self)

    @classmethod
    def broadcast(cls):
        print("Writing to clients")
        for client in cls.clients:
            client.write_message("Hi there!")


application = tornado.web.Application([
  (r'/websocket', WSHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=15), WSHandler.broadcast)
    tornado.ioloop.IOLoop.instance().start()
