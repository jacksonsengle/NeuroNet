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
import game

this_game = game.Game()

class WSHandler(tornado.websocket.WebSocketHandler):
    def set_client(self, cl):
        this_game.add_client(cl)

    def get_client(self):
        return this_game.clients.get(hash(self), None)

    def remove_client(self):
        this_game.remove_client(self.get_client())

    def check_origin(self, origin):
        return True

    def open(self):
        new_client = game.Client(socket=self)
        WSHandler.broadcast('{} has joined!'.format(new_client.user.name))
        self.set_client(new_client)

    def on_message(self, message):
        client = self.get_client()
        try:
            this_game.on_message(client, message)
        except Exception as e:
            self.broadcast("{} casued an error! (Error: {})".format(client.user.name, e))

    def on_close(self):
        self.remove_client()

    @classmethod
    def broadcast(cls, msg):
        for client_id in this_game.clients:
            client = this_game.clients[client_id]
            client.socket.write_message(msg)

this_game.ws_handler = WSHandler

application = tornado.web.Application([
  (r'/websocket', WSHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
