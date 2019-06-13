import re
from collections import namedtuple
from copy import deepcopy


class Group:
    __slot__ = ('initiative', 'quantity', 'hp',
                'atk', 'atk_type', 'weak', 'immune')

    def __init__(self, init, quan, hp, atk, atk_type, weak, immune):
        self.initiative = init
        self.quantity = quan
        self.hp = hp
        self.atk = atk
        self.atk_type = atk_type
        self.weak = weak
        self.immune = immune

    def __str__(self):
        return f"{self.atk_type:>12}{self.atk:<5}"

    def __repr__(self):
        return self.__str__()


def groups_from_string(s):
    lines = s.split('\n')
    digits_re = re.compile(r"(\d+)")
    type_re = re.compile(r'does \d+ (\w+) damage')
    immune_re = re.compile(r'immune to ([, \w]+)')
    weak_re = re.compile(r'weak to ([, \w]+)')
    g_infection = []
    g_immune = []
    g = g_immune
    for line in lines:
        if not line.strip():
            g = g_infection
            continue
        if line.strip() in ['Immunes:', 'Infections:']:
            continue
        digits = [int(x) for x in digits_re.findall(line)]
        type = type_re.search(line).group(1)
        immune = []
        weak = []
        _ = immune_re.search(line)
        if _:
            immune = _.group(1).split(', ')
        _ = weak_re.search(line)
        if _:
            weak = _.group(1).split(', ')
        g.append(Group(digits[3], digits[0], digits[1], digits[2],
                       type, weak, immune))
    return g_immune, g_infection


def groups_from_file():
    with open('../inputs.txt') as f:
        s = f.read()
    return groups_from_string(s)


def calc_damage(g_spear, g_shield):
    if g_spear.atk_type in g_shield.immune:
        return 0
    damage = g_spear.atk * g_spear.quantity
    if g_spear.atk_type in g_shield.weak:
        damage *= 2
    return damage


def choose_order(x):
    return (x.quantity * x.atk, x.initiative)


def selection_order(attacker):
    def inner_order(x):
        return (calc_damage(attacker, x), x.quantity * x.atk, x.initiative)
    return inner_order


def attack_order(kv):
    return kv[1].initiative


def simulate(g_immune, g_infection):
    immune, infection = set(g_immune), set(g_infection)
    match_table = {}
    while immune and infection:
        for attacking, defending in zip([infection, immune], [immune, infection]):
            for attacker in sorted(attacking, key=choose_order, reverse=True):
                for defender in sorted(defending, key=selection_order(attacker), reverse=True):
                    if defender not in match_table and calc_damage(attacker, defender) > 0:
                        match_table[defender] = attacker
                        break
        for defender, attacker in sorted(match_table.items(), key=attack_order, reverse=True):
            if attacker.quantity <= 0:
                continue
            damage = calc_damage(attacker, defender)
            dead_units = damage // defender.hp
            defender.quantity -= dead_units
            # print(f"{attacker}->{defender}\t does {damage}\tkilling {dead_units}")
            if defender.quantity <= 0:
                immune.discard(defender)
                infection.discard(defender)
        match_table.clear()

    left = immune or infection
    army = 'immune' if immune else 'infection'
    return army, (sum(x.quantity for x in left))


def find_smallest_boost(g_immune, g_infection):
    boost = 0
    while True:
        immune, infection = deepcopy(g_immune), deepcopy(g_infection)
        boost += 1
        print(f'test boost {boost}')
        for u in immune:
            u.atk += boost
        r = simulate(immune, infection)
        if r[0] == 'immune':
            return r[1]


# part i
print(simulate(*groups_from_file())[1])
# part ii
print(find_smallest_boost(*groups_from_file()))
