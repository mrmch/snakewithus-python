import sys
import requests
import json

def usage():
    return "./connect.py <game_name> [<server_url>] [<client_url>]"

def main():
    argv = sys.argv

    if len(argv) < 2:
        usage()
        return

    game_name = argv[1]

    if len(argv) < 3:
        server = "http://172.16.20.113:8080"
    else:
        server = argv[2]

    if len(argv) < 4:
        client = 'http://localhost:8001'
    else:
        client = argv[3]


    data = {
        "player_url": client
    }

    url = server + '/game.addplayerurl/' + game_name

    print "Conencting: %s" % url

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    requests.put(url, data=json.dumps(data), headers=headers)

if __name__ == "__main__":
    main()
