# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import json
import os
import random


def _respond(response_json):
    return json.dumps(response_json)

snake_name = 'tAUntAsaurUS'

class Snake():
    def __init__(self, board, snakes, my_id):
        self.board = board
        self.snakes = snakes

        self.me = self.get_me(my_id)

        self.width = len(self.board)
        self.height = len(self.board[0])

        self.name = snake_name

    def get_head(self):
        return self.me['queue'][-1]

    def get_me(self, my_id):
        for snake in self.snakes:
            if snake['id'] == my_id:
                return snake

    def on_edge(self):
        x,y = self.get_head()

        if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
            return True
        return False

    def move_to_edge(self):
        x,y = self.get_head()

        north = y, 'n'
        east = self.width-1-y, 'e'
        south = self.height-1-x, 's'
        west = x, 'w'

        closest = min(north, east, south, west, key=lambda x: x[0])

        return closest[1]

    def next_space_wall(self, last_move):
        x, y = self.get_head()

        if last_move == 'n':
            y = y - 1
        elif last_move == 'e':
            x = x + 1
        elif last_move == 's':
            y = y + 1
        else:
            x = x - 1

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        return False

    def new_wall_direction(self, last_move):
        square = {
            'n': 'e',
            'e': 's',
            's': 'w',
            'w': 'n'
        }

        return square[last_move]

    def get_move(self):
        if self.on_edge():
            last_move = self.me['last_move']

            if self.next_space_wall(last_move):
                return self.new_wall_direction(last_move)
            else:
                return last_move

        return self.move_to_edge()

    def get_taunt(self):
        r = random.randint(0, len(self.snakes)-1)
        snake_name = self.snakes[r]['name']

        taunts = [
            'Hey %s, you smell bad!',
            '%s: your mother is a fox',
            "If I had a dollar for every time %s farted... I'd be rich!",
            'Anybody want bbq snake? %s'
        ]

        taunt = random.choice(taunts)

        return taunt % snake_name

@bottle.post('/register')
def register():

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- REGISTER ---", str(snake_name)
    print "Game ID:", request.get('game_id')
    print "Client ID:", request.get('client_id')
    print "Board:"
    print "  Width:", request.get('board').get('width')
    print "  Height:", request.get('board').get('height')
    print "----------------"

    return _respond({
        'name': snake_name,
        'head_img_url': "http://fc02.deviantart.net/fs70/f/2010/148/3/d/20x20_PNG_Icons_sword_by_JMcIvor.png"
    })


@bottle.post('/start')
def start():

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---", str(snake_name)
    print "Game ID:", request.get('game_id')
    print "Num Players:", request.get('num_players')
    print "-------------"

    return _respond({})


@bottle.post('/tick/<client_id>')
def tick(client_id):

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- TICK", request.get('turn_num'), '---', str(snake_name)
    print "Game ID:", request.get('id')
    print "Turn Num:", request.get('turn_num')
    print "Snakes:", len(request.get('snakes'))
    # print request.get('board')
    print "----------------"
    print client_id
    print request.get('snakes')

    snake = Snake(request.get('board'), request.get('snakes'), client_id)

    my_move = snake.get_move()

    taunt = snake.get_taunt()

    return _respond({
        'move': my_move,
        'message': taunt
    })


@bottle.post('/end')
def end():

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---", str(snake_name)
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})


## Runserver ##

prod_port = os.environ.get('PORT', None)

if prod_port:
    # Assume Heroku
    bottle.run(host='0.0.0.0', port=int(prod_port), server='gevent')
else:
    # Localhost
    bottle.debug(True)
    bottle.run(host='0.0.0.0', port=8001)
