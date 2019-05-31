# railroad tycoon
from copy import deepcopy
from itertools import cycle
from colorama import init, Fore, Back, Style
init()

INPUT = '../inputs.txt'
INTER = False
#INPUT = '../example.txt'
#INTER = True


def rails_from_file():
    with open(INPUT) as f:
        rails = []
        for line in f:
            line = line[:-1]
            rails.append(list(line))
        return rails


def padding_rails(rails):
    pad_rails = [[' '] * (len(rails[0]) + 2)]
    for row in rails:
        pad_rails.append([' '] + row + [' '])
    pad_rails.append([' '] * (len(rails[0]) + 2))
    return pad_rails


class Cart:
    DIRECTIONS = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
    }
    TURNS = {
        'left': [[0, 1], [-1, 0]],
        'ahead': [[1, 0], [0, 1]],
        'right': [[0, -1], [1, 0]]
    }
    DIRECTIONS_REV = {val: key for key, val in DIRECTIONS.items()}

    def __init__(self, symbol, coordinate):
        self.symbol = symbol
        self.direction = self.DIRECTIONS[symbol]
        self.position = coordinate
        self.turns = cycle(['left', 'ahead', 'right'])
        self.history = []

    def vec_add(self, vec1, vec2):
        return tuple(x+y for x, y in zip(vec1, vec2))

    def make_a_turn(self, where):
        rotate = self.TURNS[where]
        # matrix dot multiple
        vec1 = [x*self.direction[0] for x in rotate[0]]
        vec2 = [x*self.direction[1] for x in rotate[1]]
        self.direction = self.vec_add(vec1, vec2)
        self.symbol = self.DIRECTIONS_REV[self.direction]

    def set_railroad(self, railroad):
        self.railroad = railroad

    def take_a_step(self):
        self.position = self.vec_add(self.position, self.direction)
        x, y = self.position
        rail = self.railroad[x][y]

        if rail == '/':
            if self.symbol in '<>':
                self.make_a_turn('left')
            elif self.symbol in '^v':
                self.make_a_turn('right')
        elif rail == '\\':
            if self.symbol in '<>':
                self.make_a_turn('right')
            elif self.symbol in '^v':
                self.make_a_turn('left')
        elif rail == '+':
            self.make_a_turn(next(self.turns))
        elif rail in '-|':
            pass
        else:        
            print(self.history)
            raise IndexError(self.position)
        self.history.append((self.symbol, rail, self.position))


def infer_origin_rail_at(rails, i, j):
    up = rails[i-1][j] not in ' -<>'
    down = rails[i+1][j] not in ' -<>'
    left = rails[i][j-1] not in ' |^v'
    right = rails[i][j+1] not in ' |^v'
    n_exists = sum([up, down, left, right])
    if n_exists == 2:
        if up and down:
            return '|'
        elif left and right:
            return '-'
        elif (up and left) or (down and right):
            return '/'
        else:
            return '\\'
    elif n_exists == 4:
        return '+'
    else:
        if up and down:
            return '|'
        elif left and right:
            return '-'
        else:
            raise ValueError('There should be no T cross!')


def isolate_carts_and_rails():
    rails = padding_rails(rails_from_file())
    m, n = len(rails), len(rails[0])
    carts = []
    for i in range(1, m-1):
        for j in range(1, n-1):
            item = rails[i][j]
            if item in '<>^v':
                carts.append(Cart(item, (i, j)))
                rails[i][j] = infer_origin_rail_at(rails, i, j)
    for cart in carts:
        cart.set_railroad(rails)
    return rails, carts


def print_rails(rails, carts):
    canvas = deepcopy(rails)
    for cart in carts:
        x, y = cart.position
        canvas[x][y] = f"{Fore.YELLOW}{cart.symbol}{Style.RESET_ALL}"
    print('\n'.join([''.join(row) for row in canvas]))


def simulate(interact=True):
    rails, carts = isolate_carts_and_rails()
    positions = {c.position: c for c in carts}
    crashed_carts = []
    carts = set(carts)
    while True:
        if len(carts) == 1:
            x, y = list(carts)[0].position
            x0, y0 = crashed_carts[0].position
            return [(y0-1, x0-1), (y-1, x-1)]
        for cart in sorted(carts, key=lambda x: x.position):
            if cart in crashed_carts:
                continue
            positions.pop(cart.position)
            cart.take_a_step()
            if cart.position in positions:
                crashed_carts.append(cart)
                crashed_carts.append(positions[cart.position])
                positions.pop(cart.position)
            else:
                positions[cart.position] = cart
        for cc in crashed_carts:
            carts.discard(cc)
        if interact:
            print_rails(rails, carts)
            if input() == 'q':
                break


print(simulate(interact=INTER))
