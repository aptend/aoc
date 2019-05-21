rects = []
with open('../inputs.txt') as f:
    for claim in f:
        rect = claim.split(' @ ')[1].split(': ')
        rect = rect[0].split(',') + rect[1].split('x')
        rects.append(list(map(int, rect)))

canvas = [[0]*1000 for _ in range(1000)]

cnt = 0
for rect in rects:
    for x in range(rect[0], rect[0]+rect[2]):
        for y in range(rect[1], rect[1]+rect[3]):
            if canvas[x][y] == 1:
                cnt += 1
            canvas[x][y] += 1
print('puzzle one: ', cnt)

for i, rect in enumerate(rects, 1):
    overlap = False
    for x in range(rect[0], rect[0]+rect[2]):
        for y in range(rect[1], rect[1]+rect[3]):
            if canvas[x][y] != 1:
                overlap = True
    if not overlap:
        print('puzzle two: ', i)
        break
