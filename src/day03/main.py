import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

line = ''.join(lines)

total = 0
thing = re.findall(r"(?:mul\((\d\d?\d?),(\d\d?\d?)\)|(do)\(\)|(don't)\(\))", line)
is_do = True
for i in thing:
    if i[2] == "do":
        is_do = True
    elif i[3] == "don't":
        is_do = False
    else:
        if is_do:
            total += int(i[0]) * int(i[1])
print(total)
