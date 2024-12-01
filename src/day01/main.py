import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

lista = []
listb = []
for i in lines:
    a, b = i.split()
    a = int(a)
    b = int(b)
    lista.append(a)
    listb.append(b)
total = 0
lista.sort()
listb.sort()
for i, j in zip(lista, listb):
    d = max(i, j) - min(i, j)
    total += d
print(total)

counts = {}
for i in listb:
    if i not in counts:
        counts[i] = 1
    else:
        counts[i] += 1

total = 0
for i in lista:
    a = 0
    if i in counts:
        a = counts[i]
    total += a * i

print(total)
