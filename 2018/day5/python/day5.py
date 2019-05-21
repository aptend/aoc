stack = [0]

with open('../inputs.txt') as fp:
    stream = fp.read().strip()
    for ch in stream:
        if abs(ord(ch) - stack[-1]) == 32:
            stack.pop()
        else:
            stack.append(ord(ch))

print('part I: ', len(stack)-1)

refined = []
for upper in range(65, 65+26):
    tmp_stack = [0]
    for ch in stack[1:]:
        if ch == upper or ch == upper+32:
            continue
        elif abs(ch - tmp_stack[-1]) == 32:
            tmp_stack.pop()
        else:
            tmp_stack.append(ch)
    refined.append(len(tmp_stack)-1)

print('part II: ', min(refined))
