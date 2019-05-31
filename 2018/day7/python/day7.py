from copy import deepcopy


def graph_from_file():
    graph = {chr(x): set() for x in range(ord('A'), ord('A')+26)}
    with open('../inputs.txt') as f:
        for line in f:
            x, y = extract_task(line)
            graph[y].add(x)
    return graph


def extract_task(line):
    """
    >>> extract_task('Step B must be finished before step X can begin\\n')
    ('B', 'X')
    """
    parts = line.split(' ')
    return (parts[1], parts[-3])


def no_depency_tasks(graph):
    return [task for task, dep in graph.items() if len(dep) == 0]


def stable_topo_path(graph):
    _graph = deepcopy(graph)
    path = ''
    while _graph:
        task = min(no_depency_tasks(_graph))
        path += task
        _graph.pop(task)
        for key in _graph:
            _graph[key].discard(task)
    return path


def time_count(graph):
    _graph = deepcopy(graph)
    time_count = 0
    n_woker = 5
    on_doing = dict()
    while _graph:
        to_do = no_depency_tasks(_graph)
        for task in to_do:
            if len(on_doing) == n_woker:
                break
            if task not in on_doing:
                on_doing[task] = ord(task) - ord('A') + 61

        time_elapsed = min(on_doing.values())
        time_count += time_elapsed

        for task in list(on_doing.keys()):
            if on_doing[task] == time_elapsed:
                on_doing.pop(task)
                _graph.pop(task)
                for key in _graph:
                    _graph[key].discard(task)
            else:
                on_doing[task] = on_doing[task] - time_elapsed
    return time_count


graph = graph_from_file()
print(stable_topo_path(graph))
print(time_count(graph))
