import re


def settings_from_file():
    with open('../inputs.txt') as f:
        return [int(x) for x in re.findall(r'(\d+)', f.read())]


class Marble:
    def __init__(self, v, next=None, prev=None):
        self.val = v
        self.next = next
        self.prev = prev


class MarbleGame:

    def run_new_game(self, n_elfs, n_marbles):
        """
        >>> game = MarbleGame()
        >>> game.run_new_game(9, 25)
        32
        >>> game.run_new_game(10, 1618)
        8317
        >>> game.run_new_game(13, 7999)
        146373
        """
        self.reset()
        elfs_score = [0 for _ in range(n_elfs)]
        for x in range(1, n_marbles+1):
            if x % 23 == 0:
                score = self._calc_scores(x)
                elfs_score[x % n_elfs] += score
            else:
                self._insert(x)
        return max(elfs_score)

    def reset(self):
        init = Marble(0)
        init.next = init.prev = init
        self.current_marble = init

    def __init__(self):
        self.reset()

    def _insert(self, x_val):
        p = self.current_marble.next
        q = p.next
        new_node = Marble(x_val, q, p)
        p.next = new_node
        q.prev = new_node
        self.current_marble = new_node

    def _remove(self, marble: Marble):
        p, q = marble.prev, marble.next
        p.next, q.prev = q, p

    def _calc_scores(self, x_val):
        marble = self.current_marble
        for _ in range(7):
            marble = marble.prev
        self.current_marble = marble.next
        self._remove(marble)
        return x_val + marble.val


elfs, marbles = settings_from_file()

# another solution fot this problem
from collections import deque


def max_score(player_num, marble_num):
    circle = deque([0])
    scores = [0] * player_num
    for i in range(marble_num):
        marble = i + 1
        if marble % 23:
            circle.rotate(2)
            circle.append(marble)
        else:
            player = i % player_num
            circle.rotate(-7)
            scores[player] += marble + circle.pop()
    return max(scores)


import time
s1 = time.perf_counter()
print(max_score(elfs, marbles*100))
s2 = time.perf_counter()
print(f"{s2-s1:.4f}")


game = MarbleGame()
# print(game.run_new_game(elfs, marbles))
s3 = time.perf_counter()
print(game.run_new_game(elfs, marbles*100))
s4 = time.perf_counter()
print(f"{s4-s3:.4f}")
