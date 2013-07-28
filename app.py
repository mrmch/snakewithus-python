# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import json
import os
import random
import sys


def _respond(response_json):
    return json.dumps(response_json)


from hungry_snake import HungrySnake
from taunt_snake import TauntSnake

snakes = {
    'hungry': {
        'cls': HungrySnake,
        'port': 8050
    },
    'taunt': {
        'cls': TauntSnake,
        'port': 8051
    }
}

if len(sys.argv) < 2:
    print "./appy.py <snake_name>"
    sys.exit()
else:
    sn = sys.argv[1]
    port = snakes[sn]['port']
    snake_class = snakes[sn]['cls']


@bottle.post('/<snake_name>/register')
def register(snake_name):

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


@bottle.post('/<snake_name>/start')
def start(snake_name):

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---", str(snake_name)
    print "Game ID:", request.get('game_id')
    print "Num Players:", request.get('num_players')
    print "-------------"

    return _respond({})


@bottle.post('/<snake_name>/tick/<client_id>')
def tick(snake_name, client_id):

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

    snake = snake_class(request.get('board'), request.get('snakes'), client_id)

    my_move = snake.get_move()

    taunt = snake.get_taunt()

    return _respond({
        'move': my_move,
        'message': taunt
    })


@bottle.post('/<snake_name>/end')
def end(snake_name):

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---", str(snake_name)
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})

# Localhost

print 'starting %s(%s) on %s' % (sn, snake_class, port)
bottle.debug(True)
bottle.run(host='0.0.0.0', port=port)
