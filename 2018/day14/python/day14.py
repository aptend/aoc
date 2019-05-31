def q1():
    scores = [3, 7, 1, 0, 1, 0]
    xi, yi = 3, 4
    base = 540391
    while True:
        s = scores[xi] + scores[yi]
        if s >= 10:
            scores.append(1)
            s = s % 10
        scores.append(s)
        L = len(scores)
        if L > base + 10:
            print(''.join(map(str, scores[base:base+10])))
            break
        xi = (xi + 1 + scores[xi]) % L
        yi = (yi + 1 + scores[yi]) % L


def tail_match(scores, s):
    return ''.join(map(str, scores[-len(s):])) == s


def q2():
    scores = [3, 7, 1, 0, 1, 0]
    xi, yi = 3, 4
    base = 540391
    # base = 59414
    while True:
        s = scores[xi] + scores[yi]
        if s >= 10:
            scores.append(1)
            if tail_match(scores, str(base)):
                print(len(scores)-len(str(base)))
                break
            s = s % 10
        scores.append(s)
        if tail_match(scores, str(base)):
            print(len(scores)-len(str(base)))
            break
        L = len(scores)
        xi = (xi + 1 + scores[xi]) % L
        yi = (yi + 1 + scores[yi]) % L

q2()
