from collections import Counter

def checksum(stream):
    total = 0
    twos = threes = 0
    for line in stream:
        vals = Counter(line.strip()).values()
        if 2 in vals:
            twos += 1
        if 3 in vals:
            threes += 1
    return twos * threes

def closest_pair_common(stream):
    sets = []
    for line in stream:
        s = set((i, c) for i, c in enumerate(line.strip()))
        sets.append(s)
    for i in range(len(sets)):
        for j in range(i+1, len(sets)):
            common = sets[i] - sets[j]
            if len(common) <= 1:
                skip = next(iter(common))
                return ''.join(c for _, c in sorted(sets[i]) if c != skip)

def part1():
    with open('../inputs.txt') as f:
        print(checksum(f))

def part2():
    with open('../inputs.txt') as f:
        print(closest_pair_common(f))

if __name__ == "__main__":
    part1()
    part2()
