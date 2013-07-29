class Snake():
    def __init__(self, board, snakes, my_id):
        self.board = board
        self.snakes = snakes

        self.me = self.get_me(my_id)

        self.height = len(self.board)
        self.width = len(self.board[0])

        self.name = 'Snake'

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

        if x < 0 or y < 0 or x > self.width-1 or y > self.height-1:
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

    def get_taunt(self):
        return ''

    def compute_move(self, move):
        x,y = self.get_head()

        if move == 'n':
            y = y - 1
        elif move == 'e':
            x = x + 1
        elif move == 's':
            y = y + 1
        else:
            x = x - 1

        return x,y

    def bad_move(self, move):
        x, y = self.compute_move(move)

        for pos in self.me['queue']:
            if x == pos[0] and y == pos[1]:
                return True
        return False

    def move_to(self, a, b):
        x,y = self.get_head()

        x_distance = abs(x-a)
        y_distance = abs(y-b)

        move = ''

        if x_distance > y_distance:
            if x > a:
                move = 'w'
            else:
                move = 'e'
        elif y > b:
            move = 'n'
        else:
            move = 's'

        return move
