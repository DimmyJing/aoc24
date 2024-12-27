import copy
import re
import sys
from functools import lru_cache

import networkx as nx

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

grid = list(map(list, lines))

graph = nx.Graph()


def find_grid_els(grid: list[list[str]], el: str) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    for ii, i in enumerate(grid):
        for jj, j in enumerate(i):
            if j == el:
                results.append((ii, jj))
    return results


def print_grid():
    for row in grid:
        print("".join(row))


@lru_cache(maxsize=None)
def calc_cache(n: int, blink: int) -> int:
    print(n, blink)
    if blink == 0:
        return 1
    res = 0
    if n == 0:
        res += calc_cache(1, blink - 1)
    else:
        sn = str(n)
        if len(sn) % 2 == 0:
            an = sn[: len(sn) // 2]
            bn = sn[len(sn) // 2 :]
            res += calc_cache(int(an), blink - 1)
            res += calc_cache(int(bn), blink - 1)
        else:
            res += calc_cache(n * 2024, blink - 1)
    return res


# def process(line: list[int]) -> list[int]:
#     result: list[int] = []
#     for i in line:
#         if i == 0:
#             result.append(1)
#             continue
#         si = str(i)
#         if len(si) % 2 == 0:
#             ai = si[: len(si) // 2]
#             bi = si[len(si) // 2 :]
#             result.append(int(ai))
#             result.append(int(bi))
#             continue
#         else:
#             result.append(i * 2024)
#             continue
#     return result


line = list(map(int, lines[0].split()))

# for i in range(6):
#     print(i)
#     line = process(line)
# print(len(line))
# print(line)
# print(process(line))
total = 0
for i in line:
    print(i)
    total += calc_cache(i, 75)
print(total)
