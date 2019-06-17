from datetime import datetime
from collections import defaultdict
from functools import partial


def extv_time(line):
    return line[1:17]


def extv_desc(line):
    return line[19:-1]


def extv_gid(desc):
    return int(desc.split()[1][1:])


events = dict()
with open('../inputs.txt') as f:
    for line in f:
        t = datetime.strptime(extv_time(line), "%Y-%m-%d %H:%M")
        events[t] = extv_desc(line)

canvas = partial(list, [0]*60)
nap_records = defaultdict(canvas)
for t in sorted(events.keys()):
    desc = events[t]
    if "Guard" in desc:
        gid = extv_gid(desc)
        canvas = nap_records[gid]
    elif "falls" in desc:
        st = t
    elif "wakes" in desc:
        for i in range(st.minute, t.minute):
            canvas[i] += 1

hotspot_records = {
    gid: max(enumerate(canvas), key=lambda x: x[1])
    for gid, canvas in nap_records.items()
}

total_sleep = {gid: sum(canvas) for gid, canvas in nap_records.items()}
max_gid, _ = max(total_sleep.items(), key=lambda x: x[1])
hotspot = hotspot_records[max_gid][0]

winner = max(hotspot_records.items(), key=lambda kv: kv[1][1])

print(max_gid * hotspot)
print(winner[0] * winner[1][0])
