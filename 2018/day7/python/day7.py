from copy import deepcopy
from heapq import heapify, heappop, heappush


def graph_from_file():
    with open('../inputs.txt') as f:
        return graph_from_string(f.read())


def graph_from_string(s):
    """
    >>> s = '''Step B must be finished before step X can begin.
    ... Step V must be finished before step F can begin.
    ... '''
    >>> g = graph_from_string(s)
    >>> len(g) == 26
    True
    >>> g['B'], g['V']
    (['X'], ['F'])
    """
    graph = {chr(x): [] for x in range(ord('A'), ord('A')+26)}
    lines = s.split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split()
        front, rear = parts[1], parts[-3]
        graph[front].append(rear)
    return graph


def stable_topo_path(graph):
    in_degrees = {chr(x): 0 for x in range(ord('A'), ord('A')+26)}
    for out_vertices in graph.values():
        for w in out_vertices:
            in_degrees[w] += 1

    no_dep_tasks = [k for k, v in in_degrees.items() if v == 0]
    heapify(no_dep_tasks)
    order = []
    while no_dep_tasks:
        t = heappop(no_dep_tasks)
        order.append(t)
        for k in graph[t]:
            in_degrees[k] -= 1
            if in_degrees[k] == 0:
                heappush(no_dep_tasks, k)
    return order


def time_count(graph):
    in_degrees = {chr(x): 0 for x in range(ord('A'), ord('A')+26)}
    for out_vertices in graph.values():
        for w in out_vertices:
            in_degrees[w] += 1
    time_count = 0
    n_woker = 5
    no_dep_tasks = [k for k, v in in_degrees.items() if v == 0]
    on_doing = [(ord(k) - ord('A') + 61, k) for k in no_dep_tasks]
    no_dep_tasks.clear()
    while on_doing:
        time_elapsed = on_doing[0][0]
        time_count += time_elapsed

        while on_doing and on_doing[0][0] == time_elapsed:
            _, task = heappop(on_doing)
            for k in graph[task]:
                in_degrees[k] -= 1
                if in_degrees[k] == 0:
                    heappush(no_dep_tasks, k)
        for i in range(len(on_doing)):
            on_doing[i] = ((on_doing[i][0] - time_elapsed), on_doing[i][1])

        while no_dep_tasks and len(on_doing) != n_woker:
            task = heappop(no_dep_tasks)
            heappush(on_doing, (ord(task) - ord('A') + 61, task))
    return time_count


graph = graph_from_file()
print(stable_topo_path(graph))
print(time_count(graph))
