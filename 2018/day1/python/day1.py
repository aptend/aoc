from itertools import cycle
def sum_from_stream(stream):
    total = 0
    for line in stream:
        total += int(line)
    return total

def recurrence_from_stream(stream):
    seen = set()
    result = 0
    for line in cycle(stream):
        result += int(line)
        if result in seen:
            return result
        seen.add(result)


def part1():
    with open('../inputs.txt') as f:
        print(sum_from_stream(f))

def part2():
    with open('../inputs.txt') as f:
        print(recurrence_from_stream(f))

if __name__ == "__main__":
    part1()
    part2()
