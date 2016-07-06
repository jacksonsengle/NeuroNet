#!/usr/bin/env python
"""
    game.py
    ~~~~~~~

    Game logic for NeuroNet

    :created: 2016-07-03 23:41:57 -0700
    :copyright: (c) 2016, Lambda Labs, Inc.
    :license: All Rights Reserved.
"""

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
    DIRECTIONS = set([MOVE_NORTH, MOVE_EAST, MOVE_SOUTH, MOVE_WEST])

    def __init__(self, raw_msg):
        self.name = None
        self.raw_msg = raw_msg
        self.parse_string(self.raw_msg)

    def parse_string(self, raw_string):
        self.name = self.parse_name(raw_string)
        self.msg = self.parse_msg(self.name, raw_string)

    def parse_name(self, raw_string):
        split = raw_string.split(' ', 1)
        if split[0].lower() in Command.VALID_COMMANDS:
            return split[0].lower()
        else:
            return Command.SAY

    def parse_msg(self, name, raw_string):
        if name == Command.SAY:
            split = raw_string.split(' ', 1)
            if split[0] == Command.SAY:
                return split[1]
            else:
                return raw_string
        else:
            split = raw_string.split(' ', 1)
            if len(split) > 1:
                first, rest = split
                return rest
            else:
                return split[0]

class User(object):
    def __init__(self):
        self.name = 'Somebody'
        self.location = (0, 0, 0)
    def move(self, direction):
        """
        Jackson, please implement this method, it takes in a direction in
        {Command.MOVE_NORTH, Command.MOVE_EAST, Command.MOVE_WEST, Command.MOVE_WEST}
        and updates the user's location attribute
        """
        pass

class Game(object):
    def __init__(self):
        self.clients = {}
        self.ws_handler = None

    def add_client(self, c):
        print("Adding client {} with hash {} to {}".format(c, hash(c.socket), self.clients))
        self.clients[hash(c.socket)] = c
        print(self.clients)
        self.broadcast('{} has joined!'.format(c.user.name))

    def remove_client(self, c):
        if hash(c) in self.clients:
            del self.clients[hash(c.socket)]

    def on_message(self, c, msg):
        self.perform_command(c, Command(raw_msg=msg))

    def broadcast(self, msg):
        self.ws_handler.broadcast(msg)

    def look_string(self):
        """
        Jackson, please implement this method too.
        """
        return 'You see nothing.'

    def perform_command(self, client, command):
        user = client.user
        if command.name == Command.SAY:
            self.broadcast('{} says "{}"'.format(user.name, command.msg))
        elif command.name == Command.EMOTE:
            self.broadcast('*{} {}*'.format(user.name, command.msg))
        elif command.name == Command.NAME:
            old_name = user.name
            user.name = command.msg
            self.broadcast('{} changed their name to {}.'.format(old_name, user.name))
        elif command.name == Command.INVENTORY:
            client.socket.write_message('Your inventory is empty.')
        elif command.name in set(Command.DIRECTIONS):
            client.user.move(command.name)
        elif command.name == Command.QUIT:
            pass
        elif command.name == Command.LOOK:
            self.broadcast('{} looks around.'.format(user.name))
            client.socket.write_message(self.look_string())
        else:
            pass
