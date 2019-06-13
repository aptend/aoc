def points_from_string(s):
    lines = s.split('\n')
    points = []
    for line in lines:
        if not line.strip():
            continue
        points.append(tuple(int(x) for x in line.split(',')))
    return points

def points_from_file():
    with open('../inputs.txt') as f:
        s = f.read()
    return points_from_string(s)


def classify(points):
    classes = []
    for p in points:
        clusters = []
        for c in classes:
            for q in c:
                if sum(abs(p[i]-q[i]) for i in range(4)) <= 3:
                    clusters.append(c)
                    break
        new_class = set()
        new_class.add(p)
        if not clusters:
            classes.append(new_class)
        else:
            for c in clusters:
                new_class |= c
                classes.remove(c)
            classes.append(new_class)
    return len(classes)

print(classify(points_from_string("""\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
""")))

print(classify(points_from_string("""\
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
""")))

print(classify(points_from_file()))
