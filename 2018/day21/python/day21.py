r5 = 0
possibilities = set()
while True:
    r3 = r5 | 0x10000
    r5 = 521363
    while r3:
        r5 += r3 & 0xff
        r5 &= 0xffffff
        r5 *= 65899
        r5 &= 0xffffff
        # if r3 < 256:
        #     break
        r3 >>= 8
    # part 1
    # print(r5)
    # break

    # part 2
    print(r5)
    if r5 in possibilities:
        break
    else:
        possibilities.add(r5)






