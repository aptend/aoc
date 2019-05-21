from itertools import chain
from collections import Counter, namedtuple

Box = namedtuple('Box', 'left right top bottom')


def mah_dis(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def bounding_box(points):
    """
    >>> bounding_box([
    ...    (1, 1),
    ...    (1, 6),
    ...    (8, 3),
    ...    (3, 4),
    ...    (5, 5),
    ...    (8, 9)
    ... ])
    [1, 8, 1, 9]
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return Box(min(xs), max(xs), min(ys), max(ys))


def who_rule(place, points):
    """
    >>> points = [
    ...    (1, 1),
    ...    (1, 6),
    ...    (8, 3),
    ...    (3, 4),
    ...    (5, 5),
    ...    (8, 9)
    ... ]
    >>> who_rule((1,2), points)
    (1, 1)
    >>> who_rule((1,4), points)

    >>> who_rule((5,5), points)
    (5, 5)
    """
    if not points:
        return None
    result = sorted([(mah_dis(p, place), p) for p in points])
    if len(result) > 1 and result[0][0] == result[1][0]:
        return None
    else:
        return result[0][1]


def closet_grid(points):
    box = bounding_box(points)
    w, h = box.right-box.left+1, box.bottom-box.top+1
    grid = [[None] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            grid[i][j] = who_rule((j+box.left, i+box.top), points)
    return grid


def infinite_points(closet_grid):
    m, n = len(closet_grid), len(closet_grid[0])
    inf_points = set()
    for i in range(m):
        inf_points.add(closet_grid[i][0])
        inf_points.add(closet_grid[i][n-1])
    for j in range(n):
        inf_points.add(closet_grid[0][j])
        inf_points.add(closet_grid[m-1][j])
    return inf_points


def count_max_area(closet_grid):
    inf_points = infinite_points(closet_grid)
    count = Counter(chain.from_iterable(closet_grid))
    for point, cnt in count.most_common():
        if point not in inf_points:
            return cnt


def points_from_file():
    points = []
    with open('../inputs.txt') as f:
        for line in f:
            p = line.split(', ')
            points.append((int(p[0]), int(p[1])))
    return points


def safe_region(points):
    cnt = 0
    box = bounding_box(points)
    for i in range(box.left, box.right+1):
        for j in range(box.top, box.bottom+1):
            if sum([mah_dis((i, j), p) for p in points]) < 10000:
                cnt += 1
    return cnt


points = points_from_file()
# part i
print(count_max_area(closet_grid(points)))

# part ii
print(safe_region(points))
