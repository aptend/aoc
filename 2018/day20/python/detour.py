def dfs(path):
    """
    dfs('(E(NS|)(SN|)EE(NSN|SS)EE)')[0]
    8
    dfs('(WNS(NNNNSSSS|))')[0]
    7
    dfs('(ENWWW(NEEE|SSE(EE|N)))')[0]
    10
    dfs('(ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN)')[0]
    18
    dfs('(ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE))))')[0]
    23
    dfs('(WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS)))))')[0]
    31
    """
    cnt, i = 0, 0
    fork1 = None
    fork2 = 0
    while i < len(path):
        ch = path[i]
        if ch == '(':
            c, l = dfs(path[i+1:])
            i += l
            if path[i-1] == '|':
                fork1 = c if fork1 is None else max(fork1, c)
            else:
                cnt += c
        elif ch == '|':
            other_c, other_l = dfs(path[i+1:])
            if fork1:
                cnt += max(fork1, fork2)
            if other_c == 0:
                return cnt // 2, i+2
            else:
                return max(cnt, other_c), i+1+other_l
        elif ch == ')':
            if fork1:
                cnt += max(fork1, fork2)
            return cnt, i+1
        else:
            if fork1:
                fork2 += 1
            else:
                cnt += 1
        i += 1
    return cnt, i


def max_path(path):
    """
    >>> max_path('oo(ooo|o)o')
    (6, 10)
    >>> max_path('oo(oo|oo(o|oo)oo|o)o')
    (9, 20)
    """
    candidates = []
    current_len = 0
    i = 0
    while i < len(path):
        ch = path[i]
        if ch == '(':
            max_length, consumed = max_path(path[i+1:])
            current_len += max_length
            i += consumed
        elif ch == '|':
            candidates.append(current_len)
            current_len = 0
        elif ch == ')':
            candidates.append(current_len)
            return max(candidates), i+1
        else:  # element
            current_len += 1
        i += 1
    candidates.append(current_len)
    return max(candidates), i


def max_path_ii(path):
    """
    >>> max_path_ii('oo(oooo|)o')
    4
    >>> max_path_ii('oo(oo|)(oooo|)ooo')
    5
    """
    current_len = 0
    i = 0
    while i < len(path):
        ch = path[i]
        if ch == '(':
            j = i
            while j < len(path) and path[j] != '|':
                j += 1
            fork1 = (j - i - 1) // 2
            fork2 = max_path_ii(path[j+2:])
            current_len += max(fork1, fork2)
            return current_len
        else:  # element
            current_len += 1
        i += 1
    return current_len
