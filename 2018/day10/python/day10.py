def points_from_file():
    with open('../inputs.txt') as f:
        xs, ys, vs = [], [], []
        for line in f:
            xs.append(int(line[10:16]))
            ys.append(int(line[18:24]))
            vs.append((int(line[36:38]), int(line[40:42])))
        return xs, ys, vs


def tick(xs, ys, vs):
    w, h = 100, 12
    t = 0
    while True:
        t += 1
        for i in range(len(xs)):
            xs[i] += vs[i][0]
            ys[i] += vs[i][1]
        low_xs, up_xs = min(xs), max(xs)
        low_ys, up_ys = min(ys), max(ys)
        if up_xs - low_xs < w and up_ys - low_ys < h:
            canvas = [[' '] * w for _ in range(h)]
            for x, y in zip(xs, ys):
                canvas[y-low_ys][x-low_xs] = '#'
            print(f"{t} seconds later")
            print('\n'.join(''.join(line) for line in canvas))
            if input("> next? ") == 'q':
                break


tick(*points_from_file())
