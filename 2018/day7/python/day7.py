from collections import defaultdict


def graph_from_file():
    graph = defaultdict(list)
    with open('../inputs.txt') as f:
        for line in f:
            x, y = extract_task(line)
            graph[y].append(x)
    for k in graph.keys():
        graph[k] = sorted(graph[k])
    return graph


def extract_task(line):
    """
    >>> extract_task('Step B must be finished before step X can begin\\n')
    ('B', 'X')
    """
    parts = line.split(' ')
    return (parts[1], parts[-3])


def has_cycle(graph):
    """
    >>> has_cycle({'A':['B', 'C'], 'B':[], 'C':['A']})
    True
    >>> has_cycle({'A':['B', 'C'], 'B':[], 'C':['B']})
    False
    """
    seen = set()
    stack = set()

    def dfs(key):
        if key in stack:
            return True
        if key in seen:
            return False
        seen.add(key)
        stack.add(key)
        for next_ in graph[key]:
            if dfs(next_):
                return True
        stack.remove(key)
        return False

    for key in graph:
        if dfs(key):
            return True
    return False


def topo_path(graph):
    seen = set()
    path = []

    def dfs(key, path):
        if key in seen:
            return
        seen.add(key)
        for next_ in graph[key]:
            dfs(next_, path)
        path.append(key)

    for key in sorted(graph.keys()):
        dfs(key, path)

    return ''.join(path)


graph = graph_from_file()
print(topo_path(graph))
