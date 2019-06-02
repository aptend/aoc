from copy import deepcopy

def area_from_file():
    with open('../inputs.txt') as f:
        return area_from_string(f.read())


def area_from_string(s):
    area = []
    for line in s.split('\n'):
        if not line.strip():
            continue
        area.append(list(line))
    return area
    

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def run(area):
    m, n = len(area), len(area[0])
    for r in range(800):
        next_round = deepcopy(area)
        for i in range(m):
            for j in range(n):
                _open = 0
                _lumberyard = 0
                _wood = 0
                for di, dj in DIRECTIONS:
                    ni, nj = i+di, j+dj
                    if -1 < ni < m and -1 < nj < n:
                        item = area[ni][nj]
                        if item == '.':
                            _open += 1
                        elif item == '|':
                            _wood += 1
                        else:
                            _lumberyard += 1
                here = area[i][j]
                if here == '.' and _wood >= 3:
                    next_round[i][j] = '|'
                elif here == '|' and _lumberyard >= 3:
                    next_round[i][j] = '#'
                elif here == '#' and (_lumberyard == 0 or _wood == 0):
                    next_round[i][j] ='.'
        area = next_round
       
        wood = 0
        lumberyard = 0
        for row in area:
            for ch in row:
                if ch == '|':
                    wood += 1
                elif ch == '#':
                    lumberyard += 1
        print(wood* lumberyard, r)

example = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

# run(area_from_string(example))
run(area_from_file())
# repeat
# 77822 500
# 80948 501
# 85910 502
# 90155 503
# 95232 504
# 97782 505
# 101840 506
# 105183 507
# 103880 508
# 103970 509
# 101802 510
# 97350 511
# 94579 512
# 89436 513
# 91581 514
# 87250 515
# 88893 516
# 92232 517
# 96012 518
# 98814 519
# 100466 520
# 101840 521
# 103224 522
# 102366 523
# 97270 524
# 92839 525
# 91425 526
# 88894 527
# 86320 528
# 82984 529
# 81788 530
# 78324 531
# 77361 532
# 76874 533
# 77315 534

