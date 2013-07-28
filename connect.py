import sys
import requests
import json

def usage():
    return "./connect.py <game_name> [<snake_name>] [<server_url>] [<client_url>]"

def main():
    argv = sys.argv

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

    if len(argv) < 2:
        usage()
        return

    game_name = argv[1]

    if len(argv) < 3:
        snake_name = 'taunt'
    else:
        snake_name = argv[2]

    port = snakes[snake_name]['port']

    if len(argv) < 4:
        server = "http://172.16.20.113:8080"
    else:
        server = argv[3]

    if len(argv) < 5:
        client = 'http://172.16.20.113:%s/%s' % (port, snake_name)
    else:
        client = argv[4]

    data = {
        "player_url": client
    }

    url = server + '/game.addplayerurl/' + game_name

    print "Conencting: %s" % url

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    requests.put(url, data=json.dumps(data), headers=headers)

if __name__ == "__main__":
    main()
