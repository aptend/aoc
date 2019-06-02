from collections import defaultdict, namedtuple
Sample = namedtuple('Sample', 'raw ins result')


def op_addi(R, a, b, c):
    R[c] = R[a] + b


def op_addr(R, a, b, c):
    R[c] = R[a] + R[b]


def op_muli(R, a, b, c):
    R[c] = R[a] * b


def op_mulr(R, a, b, c):
    R[c] = R[a] * R[b]


def op_bani(R, a, b, c):
    R[c] = R[a] & b


def op_banr(R, a, b, c):
    R[c] = R[a] & R[b]


def op_bori(R, a, b, c):
    R[c] = R[a] | b


def op_borr(R, a, b, c):
    R[c] = R[a] | R[b]


def op_seti(R, a, b, c):
    R[c] = a


def op_setr(R, a, b, c):
    R[c] = R[a]


def op_gtir(R, a, b, c):
    R[c] = 1 if a > R[b] else 0


def op_gtri(R, a, b, c):
    R[c] = 1 if R[a] > b else 0


def op_gtrr(R, a, b, c):
    R[c] = 1 if R[a] > R[b] else 0


def op_eqir(R, a, b, c):
    R[c] = 1 if a == R[b] else 0


def op_eqri(R, a, b, c):
    R[c] = 1 if R[a] == b else 0


def op_eqrr(R, a, b, c):
    R[c] = 1 if R[a] == R[b] else 0


FUNCS = [val for key, val in locals().items() if key.startswith('op_')]


def full_op_name_set():
    return set([func.__name__ for func in FUNCS])


def samples_from_file():
    with open('../inputs1.txt') as f:
        lines = f.readlines()
    samples = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('Before'):
            raw = [int(lines[i][d]) for d in (9, 12, 15, 18)]
            i += 1
            ins = list(map(int, lines[i].strip().split()))
            i += 1
            result = [int(lines[i][d]) for d in (9, 12, 15, 18)]
            samples.append(Sample(raw, ins, result))
        else:
            i += 1
    return samples


def count_three_more(samples):
    three_or_more = 0

    for sample in samples:
        cnt = 0
        for func in FUNCS:
            R = sample.raw[:]
            func(R, *sample.ins[1:])
            if R == sample.result:
                cnt += 1
            if cnt >= 3:
                three_or_more += 1
                break
    return three_or_more


def infer_op_name(samples):
    instructions = defaultdict(full_op_name_set)
    candidates = set()
    for sample in samples:
        op_num = sample.ins[0]
        for func in FUNCS:
            R = sample.raw[:]
            func(R, *sample.ins[1:])
            if R == sample.result:
                candidates.add(func.__name__)
        instructions[op_num] &= candidates
        candidates.clear()

    op_mapping = {}
    while instructions:
        certain_names = set()
        for key, val in instructions.items():
            if len(val) == 1:
                certain_name = list(val)[0]
                op_mapping[key] = certain_name
                certain_names.add(certain_name)
        new_ins = dict()
        for key in instructions:
            if key not in op_mapping:
                new_ins[key] = instructions[key] - certain_names
        instructions = new_ins
    return op_mapping


samples = samples_from_file()
print(count_three_more(samples))

op_mapping = infer_op_name(samples)

with open('../inputs2.txt') as f:
    ins = []
    for line in f:
        ins.append([int(d) for d in line.strip().split()])

R = [0, 0, 0, 0]
for i in ins:
    op_num = i[0]
    vals = i[1:]
    name = op_mapping[op_num]
    locals()[name](R, *vals)
print(R[0])
