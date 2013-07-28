from base_snake import Snake

class TauntSnake(Snake):
    name = 'TauntSnake'

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
