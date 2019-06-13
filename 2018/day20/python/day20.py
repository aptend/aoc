with open('../inputs.txt') as f:
    path = f.read()[:-1]

path = f"({path[1:-1]})"

def travel(ins):
    """
    >>> travel('E(NS|)(SN|)EE(NEN|SS)EE')
    8
    >>> travel('WNE(NNNNSSSS|)')
    7
    >>> travel('ENWWW(NEEE|SSE(EE|N))')
    10
    >>> travel('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN')
    18
    >>> travel('ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))')
    23
    >>> travel('WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))')
    31
    """
    i = 0
    x, y = 0, 0
    stack = [(x, y)]
    n_forks = 0
    forks_stack = [n_forks]
    steps = 0
    rooms = {(x, y): steps}
    farest = 0
    overthere_cnt = 0
    while i < len(ins):
        ch = ins[i]
        if ch == '(':
            stack.append((x, y))
            forks_stack.append(n_forks)
            n_forks = 0
        elif ch == '|':
            if ins[i+1] == ')':
                i += 1
                x, y = stack.pop()
                n_forks = forks_stack.pop()
                steps = rooms[(x, y)]
            else:
                stack.append((x, y))
                n_forks += 1
                x, y = stack[-1 - n_forks]
                steps = rooms[(x, y)]
        elif ch == ')':
            for _ in range(n_forks):
                fork = stack.pop()
                if rooms[fork] > steps:
                    x, y = fork
                    steps = rooms[fork]
            stack.pop()
            n_forks = forks_stack.pop()
        else:
            if ch == 'E':
                x += 1
            elif ch == 'W':
                x -= 1
            elif ch == 'N':
                y += 1
            else:
                y -= 1
            if (x, y) not in rooms:
                steps += 1
                if steps > farest:
                    farest = steps
                if steps >= 1000:
                    overthere_cnt += 1
                rooms[(x, y)] = steps
            else:
                steps = rooms[(x, y)]
        i += 1
    return farest, overthere_cnt


print(travel('E(NS|)(SN|)EE(NEN|SS)EE'))
print(travel(path))
