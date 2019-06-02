from copy import deepcopy


class Soldier:
    __slot__ = ('role', 'position', 'HP', 'ATK')

    def __init__(self, role, position, hp, attack):
        self.role = role
        self.position = position
        self.HP = hp
        self.ATK = attack

    def find_best_target(self, env):
        rival = None
        i, j = self.position
        for di, dj in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            unit = env[i+di][j+dj]
            # not a soldier or is a teammate
            if not unit or unit.role == self.role:
                continue
            if not rival or unit.HP < rival.HP:
                rival = unit
        return rival

    def attack(self, rival):
        rival.HP -= self.ATK


class BattleField:
    def __init__(self):
        self.land_map = []
        self.soldier_map = []
        self.Gs = set()
        self.Es = set()
        self.soldier_factory = test_atk(3)

    def show_battle(self):
        canvas = deepcopy(self.land_map)
        for i, j, unit in self._soldier_map_iter():
            if unit:
                canvas[i][j] = unit.role
        s = '\n'.join(''.join(row) for row in canvas) + '\n'
        s += f'G HP: {sorted([x.HP for x in self.Gs])}\n'
        s += f'E HP: {sorted([x.HP for x in self.Es])}\n'
        return s

    def set_soldier_factory(self, factory):
        self.soldier_factory = factory

    def _is_game_end(self):
        if len(self.Gs) == 0 or len(self.Es) == 0:
            return True
        return False

    def _soldier_map_iter(self):
        for i in range(len(self.soldier_map)):
            for j in range(len(self.soldier_map[0])):
                yield i, j, self.soldier_map[i][j]

    def init_from_string(self, s):
        for i, line in enumerate(s.split('\n')):
            if not line:
                continue
            self.land_map.append([None]*len(line))
            self.soldier_map.append([None]*len(line))
            for j, ch in enumerate(line):
                if ch in 'EG':
                    soldier = self.soldier_factory(ch, (i, j))
                    self.soldier_map[i][j] = soldier
                    self.land_map[i][j] = '.'
                else:
                    self.land_map[i][j] = ch
        # diff parties
        for _, _, unit in self._soldier_map_iter():
            if not unit:
                continue
            if unit.role == 'G':
                self.Gs.add(unit)
            else:
                self.Es.add(unit)

    def _clean_body(self, body):
        i, j = body.position
        self.soldier_map[i][j] = None
        if body.role == 'G':
            self.Gs.remove(body)
        else:
            self.Es.discard(body)

    def search_and_attack(self, soldier):
        rival = soldier.find_best_target(self.soldier_map)
        if rival:
            soldier.attack(rival)
            if rival.HP <= 0:
                self._clean_body(rival)
            return True
        return False

    def shortest_path_between(self, p1, p2):
        """
        >>> field = BattleField()
        >>> field.init_from_string(\"\"\"\\
        ... #######
        ... #E....#
        ... #...#.#
        ... #.G.#G#
        ... #######
        ... \"\"\")
        >>> field.shortest_path_between((3,3), (3,5))
        [(2, 5), (1, 5), (1, 4), (1, 3), (2, 3)]
        """
        seen = {p1: None}
        openlist = [p1]
        # iterate by insertation order
        # insert by reading order
        for p in openlist:
            for di, dj in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                i, j = (p[0]+di, p[1]+dj)
                next_p = (i, j)
                if next_p == p2:
                    path = []
                    while p:
                        path.append(p)
                        p = seen[p]
                    path.pop()  # remove start point
                    return path
                if (next_p in seen or
                        self.land_map[i][j] != '.' or
                        self.soldier_map[i][j]):
                    continue
                seen[next_p] = p
                openlist.append(next_p)
        return None

    def move(self, soldier):
        rivals = self.Es if soldier.role == 'G' else self.Gs
        candidates = []
        for rival in rivals:
            path = self.shortest_path_between(soldier.position, rival.position)
            if path:
                # sorted by (steps, reading order, first_step)
                candidates.append((len(path), rival.position, path[-1]))
        if candidates:
            ni, nj = sorted(candidates)[0][2]
            i, j = soldier.position
            self.soldier_map[i][j] = None
            soldier.position = (ni, nj)
            self.soldier_map[ni][nj] = soldier

    def run_round(self):
        handled_units = set()
        for _, _, unit in self._soldier_map_iter():
            if not unit or unit in handled_units:
                continue
            # take this turn to attack
            if self.search_and_attack(unit):
                continue
            # take this turn to move and try to attack
            # combat only ends when solider find no rivals
            if self._is_game_end():
                return False
            self.move(unit)
            self.search_and_attack(unit)
            handled_units.add(unit)
        return True

    def simulate(self):
        _round = 0
        while True:
            go_on = self.run_round()
            if SHOW:
                if go_on:
                    print(f"~~~~~~~after {_round+1} round~~~~~~~~~\n")
                else:
                    print(f"=======combat ends in {_round+1} round=======\n")
                print(self.show_battle())
                if INTERACT and input() == 'q':
                    go_on = False
            if not go_on:
                break
            _round += 1

        winner = self.Es if len(self.Gs) == 0 else self.Gs
        total_HP = sum([x.HP for x in winner])
        return _round * total_HP


def test_atk(n):
    def soldier_factory(role, position):
        if role == 'E':
            return Soldier(role, position, 200, n)
        else:
            return Soldier(role, position, 200, 3)
    return soldier_factory

with open('../inputs.txt') as f:
    big_war = f.read()

SHOW = True
INTERACT = False


battle = BattleField()
battle.init_from_string(big_war)
print(battle.simulate())

# part II
# for i in range(4, 30):
#     battle = BattleField()
#     battle.set_soldier_factory(test_atk(i))
#     battle.init_from_string(big_war)
#     r = battle.simulate()
#     if len(battle.Es) == 10:
#         print(f"minimum atk {r!r} for elfs to win with 0 loss")
#         break
