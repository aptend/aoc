# depth = 510
# m = 10
# n = 10

from heapq import heappop, heappush
depth = 11109
m = 9
n = 731

padding = 20

pm, pn = m + padding, n + padding

cave = [[None] * pm for _ in range(pn)]
erosion_lv = [[None] * pm for _ in range(pn)]
for i in range(pn):
    for j in range(pm):
        if (i == 0 and j == 0) or (i == n and j == m):
            geo_idx = 0
        elif i == 0:
            geo_idx = j * 16807
        elif j == 0:
            geo_idx = i * 48271
        else:
            geo_idx = erosion_lv[i-1][j] * erosion_lv[i][j-1]
        lv = (geo_idx + depth) % 20183
        erosion_lv[i][j] = lv
        cave[i][j] = lv % 3

# part i
print(sum(cave[i][j] for i in range(n+1) for j in range(m+1)))


class Edge:
    __slot__ = ('src', 'to', 'weight')

    def __init__(self, src, to, weight):
        self.src = src
        self.to = to
        self.weight = weight


class Graph:
    def __init__(self, v):
        self.V = v
        self.adj = [[] for _ in range(v)]

    def add_edge(self, edge):
        self.adj[edge.src].append(edge)

# 0: rocky  [torch gear]
# 1: wet    [gear neither]
# 2: narrow [torch neither]


# delta[0][1] means 
# (rocky[0] -> wet[0], # rocky with torch -> wet with gear
#  rocky[0] -> wet[1],
#  rocky[1] -> wet[0],
#  rocky[1] -> wet[1])

deltas = [
    [(1, None, None, 1), (None, None, 1, None), (1, None, None, None)],
    [(None, 1, None, None), (1, None, None, 1), (None, None, None, 1)],
    [(1, None, None, None), (None, None, None, 1), (1, None, None, 1)],
]
edge_order = [(0, 0), (0, 1), (1, 0), (1, 1)]
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

g = Graph(pm * pn * 2)
for i in range(pn):
    for j in range(pm):
        src = (i * pm + j) * 2
        src_type = cave[i][j]
        g.add_edge(Edge(src, src+1, 7))
        g.add_edge(Edge(src+1, src, 7))
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if not (-1 < ni < pn and -1 < nj < pm):
                continue
            to = (ni * pm + nj) * 2
            to_type = cave[ni][nj]
            delta = deltas[src_type][to_type]
            for idx, weight in enumerate(delta):
                if weight is None:
                    continue
                d1, d2 = edge_order[idx]
                g.add_edge(Edge(src+d1, to+d2, weight))

# import sys
# sys.exit(0)
def whereami(x):
    order, tool = divmod(x, 2)
    i, j = divmod(order, pm)
    return i, j, tool


def sp(g):
    dist_to = [float('inf')] * g.V
    dist_to[0] = 0
    edge_to = [None] * g.V
    seen = set()
    heap = [(0, 0)]
    target = (n * pm + m) * 2
    while heap:
        dist, v = heappop(heap)
        if v == target:
            x = v
            path = []
            while x:
                path.append(whereami(x))
                x = edge_to[x]
            path.reverse()
            return dist, path
        if v in seen:
            continue
        seen.add(v)
        for e in g.adj[v]:
            w = e.to
            if dist_to[w] > dist_to[v] + e.weight:
                dist_to[w] = dist_to[v] + e.weight
                edge_to[w] = v
                heappush(heap, (dist_to[w], w))

steps, path = sp(g)
print(steps)
