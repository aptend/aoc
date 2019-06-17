from collections import namedtuple

State = namedtuple('State', 'content origin')


def rules_from_file():
    """
    return  
    initial: State, State('##.......#.######.##..#', 0)    
    live_patterns: set(<str>), {##.##', '..#.#'}
    """
    with open('../inputs.txt') as f:
        initial = ''
        live_patterns = set()
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('initial'):
                initial = State(line.split(': ')[1], 0)
            else:
                parts = line.split(' => ')
                if parts[1] == '#':
                    live_patterns.add(parts[0])
        return initial, live_patterns


def padding_state(state):
    """
    >>> padding_state(State('#..#..#..', 0))
    State(content='...#..#..#...', origin=3)
    >>> padding_state(State('.......#..#..#.....', 0))
    State(content='...#..#..#...', origin=-4)
    """
    c = state.content
    left, right = c.find('#'), c.rfind('#')
    return State(f"...{c[left:right+1]}...", state.origin + 3 - left)


def grow(state, live_patterns):
    pad_content = f"..{state.content}.."
    formed = []
    for i in range(2, len(pad_content)-2):
        if pad_content[i-2:i+3] in live_patterns:
            formed.append('#')
        else:
            formed.append('.')
    return State(''.join(formed), state.origin)


def foresee(state, live_patterns, generations):
    """
    >>> s = State('#..#.#..##......###...###', 0)
    >>> ptrns = set(['...##',
    ... '..#..',
    ... '.#...',
    ... '.#.#.',
    ... '.#.##',
    ... '.##..',
    ... '.####',
    ... '#.#.#',
    ... '#.###',
    ... '##.#.',
    ... '##.##',
    ... '###..',
    ... '###.#',
    ... '####.'])
    >>> foresee(s, ptrns, 20)
    State(content='...#....##....#####...#######....#.#..##..', origin=5)
    """
    s = state
    for _ in range(generations):
        s = grow(padding_state(s), live_patterns)
    return s


def count_plant_pots(state):
    """
    >>> count_plant_pots(State('.#....##....#####...#######....#.#..##.', 3))
    325
    """
    return sum(i-state.origin for i, c in enumerate(state.content) if c == '#')


state, live_patterns = rules_from_file()
print(count_plant_pots(foresee(state, live_patterns, 20)))

# after 98 generations, total number increases at a constant speed of 40 per gen
print(count_plant_pots(foresee(state, live_patterns, 100)) + (50000000000 - 100)*40)
