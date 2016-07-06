#!/usr/bin/env python
"""
    game.py
    ~~~~~~~

    Game logic for NeuroNet

    :created: 2016-07-03 23:41:57 -0700
    :copyright: (c) 2016, Lambda Labs, Inc.
    :license: All Rights Reserved.
"""

class User(object):
    def __init__(self):
        self.name = 'Somebody'
        self.location = (0, 0, 0)

class Client(object):
    def __init__(self, socket):
        self.socket = socket
        self.user = User()

class Command(object):
    SAY = 'say'
    EMOTE = 'emote'
    NAME = 'name'
    LOOK = 'look'
    INVENTORY = 'inventory'
    MOVE_NORTH = 'north'
    MOVE_EAST = 'east'
    MOVE_SOUTH = 'south'
    MOVE_WEST = 'west'
    QUIT = 'quit'
    VALID_COMMANDS = set([SAY, EMOTE, NAME, INVENTORY, MOVE_NORTH, MOVE_EAST,
                          MOVE_SOUTH, MOVE_WEST, QUIT, LOOK])
    def __init__(self, raw_msg):
        self.name = None
        self.raw_msg
        self.parse_string(self.raw_msg)

    def parse_string(self, raw_string):
        self.name = self.parse_name(raw_string)
        self.msg = self.parse_msg(raw_string)

    def parse_name(self, raw_string):
        first, rest = raw_string.split(' ', 1)
        if f.lower() in Command.VALID_COMMANDS:
            return f.lower()
        raise Exception("Invalid command {}.".format(self.name))

    def parse_msg(self, raw_string):
        first, rest = raw_string.split(' ', 1)
        return rest

class Game(object):
    def __init__(self):
        self.clients = {}
        self.ws_handler = None

    def add_client(self, c):
        self.clients[hash(c)] = c
        self.broadcast('{} has joined!'.format(new_client.user.name))

    def remove_client(self, c):
        del self.clients[hash(c)]

    def on_message(self, c, msg):
        self.perform_command(c, Command(msg=msg))

    def broadcast(self, msg):
        self.ws_handler.broadcast(msg)

    def look_string(self):
        return 'You see nothing.'

    def perform_command(self, client, command):
        if command.name == SAY:
            self.broadcast('{} says "{}"'.format(user.name, command.msg))
        elif command.name == EMOTE:
            self.broadcast('{} {}'.format(user.name, command.msg))
        elif command.name == NAME:
            old_name = user.name
            user.name = command.msg
            self.broadcast('{} changed their name to {}.'.format(old_name, user.name))
        elif command.name == INVENTORY:
            client.socket.write_message('Your inventory is empty.')
        elif command.name == MOVE_NORTH:
            pass
        elif command.name == MOVE_EAST:
            pass
        elif command.name == MOVE_SOUTH:
            pass
        elif command.name == MOVE_WEST:
            pass
        elif command.name == QUIT:
            pass
        elif command.name == Command.SAY:
            pass
        elif command.name == Command.EMOTE:
            pass
        elif command.name == Command.LOOK:
            self.broadcast('{} looks around.'.format(user.name))
            client.socket.write_message(self.look_string())
        else:
            pass
