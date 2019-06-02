import re
from enum import Enum


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class End(Enum):
    """
    #x                x            x    
    ####  :WALL      |### :WATER   .### :EMPTY
    """
    WALL = 0
    WATER = 1
    EMPTY = 2


def lines_from_file():
    with open('../inputs.txt') as f:
        return lines_from_string(f.read())


def lines_from_string(s):
    lines = s.split('\n')
    ver_lines = []
    hor_lines = []
    regex = re.compile(r'.=(\d+), .=(\d+)[.]{2}(\d+)')
    for line in lines:
        if not line.strip():
            continue
        digits = tuple(int(x) for x in regex.search(line).groups(0))
        if line[0] == 'y':
            hor_lines.append(digits)
        else:
            ver_lines.append(digits)
    return ver_lines, hor_lines


def boundry(ver_lines, hor_lines):
    x_points = set(l[0] for l in ver_lines)
    y_points = set(l[0] for l in hor_lines)
    for line in ver_lines:
        y_points.add(line[1])
        y_points.add(line[2])
    for line in hor_lines:
        x_points.add(line[1])
        x_points.add(line[2])
    x_min, x_max = min(x_points), max(x_points)
    y_min, y_max = min(y_points), max(y_points)
    return (x_min, x_max, y_min, y_max)


def slice_map(ver_lines, hor_lines):
    xl, xr, yt, yb = boundry(ver_lines, hor_lines)
    width = xr - xl + 3  # padding left and right by 1
    depth = yb - yt + 3  # padding bottom by 1
    slice_map = [['.'] * width for _ in range(depth)]
    for line in hor_lines:
        i = line[0] - yt + 1
        for j in range(line[1]-xl+1, line[2]-xl+1+1):
            slice_map[i][j] = '#'
    for line in ver_lines:
        j = line[0] - xl + 1
        for i in range(line[1]-yt+1, line[2]-yt+1+1):
            slice_map[i][j] = '#'
    slice_map[0][500-xl+1] = '+'
    return slice_map


def level_end(slice_map, point, direction):
    i, j = point
    delta = 1 if direction == Direction.RIGHT else -1
    while True:
        j += delta
        if slice_map[i][j] == '#':
            return (i, j-delta), End.WALL
        if slice_map[i+1][j] == '|':
            return (i, j), End.WATER
        if slice_map[i+1][j] == '.':
            return (i, j), End.EMPTY


def fill_level(slice_map, point):
    i, j = point
    l_end, l_type = level_end(slice_map, point, Direction.LEFT)
    r_end, r_type = level_end(slice_map, point, Direction.RIGHT)
    fillup_char = '~' if (l_type == End.WALL and r_type == End.WALL) else '|'
    for j in range(l_end[1], r_end[1]+1):
        slice_map[i][j] = fillup_char
    l_over = True if l_type == End.WATER else False  # '|' means infinity
    r_over = True if r_type == End.WATER else False
    if l_type == End.EMPTY:
        l_over = simulate(slice_map, l_end)  # does it reach infinity?
    if r_type == End.EMPTY:
        r_over = simulate(slice_map, r_end)
    return l_over or r_over  # report the result to upper-layer simulation


def simulate(slice_map, spring):
    i, j = spring
    while i < len(slice_map)-1:
        slice_map[i][j] = '|'
        if slice_map[i+1][j] in '#~':
            break
        i += 1
    if i == len(slice_map)-1:
        # I'm the lowest simulation, and yes, I reach infinity
        return True

    for level in range(i, spring[0]-1, -1):
        over = fill_level(slice_map, (level, j))
        if over:
            # I'm middle-layer simulation, and
            # one of my following simulations has touched the face of infinity
            return True
    else:
        return False


def show_map(slice_map):
    print('\n'.join([''.join(row) for row in slice_map]))


def count_water_trace(slice_map):
    reach_tiles = -1  # subtract the ringinal spring
    keep = 0
    for row in slice_map:
        for ch in row:
            if ch in '|~':
                reach_tiles += 1
            if ch == '~':
                keep += 1
    return reach_tiles, keep


example1 = """\
x=495, y=3..5
y=7, x=495..501
y=4, x=495..498
x=501, y=3..7
x=498, y=3..4
x=506, y=1..2
x=492, y=2..13
x=496, y=9..13
y=13, x=492..495
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""

example0 = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""

# _map = slice_map(*lines_from_string(example0))
_map = slice_map(*lines_from_file())
springx = _map[0].index('+')
simulate(_map, (0, springx))
# show_map(_map)
print(count_water_trace(_map))
