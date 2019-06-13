
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


with open('../inputs21.txt') as f:
    lines = f.readlines()
    ip = int(lines[0].strip().split()[1])
    ins = []
    for line in lines[1:]:
        parts = line.strip().split()
        op_name = parts[:1]
        op_vals = [int(x) for x in parts[1:]]
        ins.append(op_name + op_vals)

R = [0] * 6  # part1
FUNCS = {k[3:]: v for k, v in locals().items() if k[:3] == 'op_'}
func = FUNCS[ins[0][0]]
func(R, *ins[0][1:])
while True:
    R[ip] += 1
    number = R[ip]
    if number > len(ins):
        break
    func = FUNCS[ins[number][0]]
    print(R, end=f' -{ins[number]}> ')
    func(R, *ins[number][1:])
    print(R)
    if input() == 'q':
        break

print(R)

# the core step are below.
# while r5 <= r4:
#     r2 = 1
#     while r2 <= r4:
#         if r2 * r5 == r4:
#             r0 += r5
#         r2 += 1
#     r5 += 1
# so this program is going to figure out the sum of all the factors of r4
# for part 1, r4 == 989 and for part 2, r4 = 10551389
