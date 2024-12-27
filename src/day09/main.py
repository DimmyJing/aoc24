import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

grid = list(map(list, lines))

line = lines[0]
thing = []

empty = False
count = 0
for i in line:
    i = int(i)
    if empty:
        for j in range(i):
            thing.append(-1)
    else:
        for j in range(i):
            thing.append(count)
        count += 1
    empty = not empty
begin_idx = 0
end_idx = len(thing) - 1

for i in range(count - 1, -1, -1):
    print(i)
    start_idx = thing.index(i)
    length = 0
    while start_idx + length < len(thing) and thing[start_idx + length] == i:
        length += 1
    good_len = 0
    good_idx = -1
    for jj, j in enumerate(thing):
        if j != -1:
            good_len = 0
        else:
            good_len += 1
        if jj >= start_idx:
            break
        if good_len == length:
            good_idx = jj - length + 1
            break
    if good_idx != -1:
        for j in range(length):
            thing[good_idx + j] = i
            thing[start_idx + j] = -1
print(thing)

while end_idx >= 0:
    if thing[end_idx] == -1:
        end_idx -= 1
        continue
    while begin_idx < len(thing) and thing[begin_idx] != -1:
        begin_idx += 1
    if begin_idx >= end_idx or begin_idx >= len(thing):
        break
    thing[begin_idx] = thing[end_idx]
    thing[end_idx] = -1
    print(end_idx)
    end_idx -= 1

total = 0
for ii, i in enumerate(thing):
    if i >= 0:
        total += ii * i
print(thing)
print(total)
