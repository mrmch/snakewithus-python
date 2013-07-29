import random

from base_snake import Snake

class HungrySnake(Snake):
    name = 'HunnnnnnnngrySnake'
    head_img_url = 'http://i.imgur.com/AJPTBN3.png'

    def find_food(self):
        food = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                for box in self.board[y][x]:
                    if box['type'] == 'food':
                        food.append((x,y))

        return food

    def find_closest(self, squares):
        x,y = self.get_head()
        d = 100000
        
        for square in squares:
            new_d = abs(square[0] - x) + abs(square[1] - y)

            if new_d < d:
                new_d = d
                a = square[0]
                b = square[1]

        return a,b
    
    def get_move(self):

        all_food = self.find_food()

        if len(all_food) > 0:
            x, y = self.find_closest(all_food)
        else:
            x = int(self.width/2)
            y = int(self.height/2)

        move = self.move_to(x, y)
        last_move = self.me['last_move']

        if (move == 'n' and last_move == 's') or \
            (move == 's' and last_move == 'n'):
            move = 'w'
        elif (move == 'w' and last_move == 'e') or \
            (move == 'e' and last_move == 'w'):
            move = 'w'

        return move

    def get_taunt(self):
        taunts = [
            'Nom nom nom',
            'Yum!',
            'That was tasty!',
            'Bleaah, apples.',
            'Nummy nummy in my tummy!'
        ]
        t = ''

        if self.me['ate_last_turn']:
            t = random.choice(taunts)

        return t
