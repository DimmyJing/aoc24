import copy
import re
import sys
import time
from functools import lru_cache

import networkx as nx

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

graph = nx.Graph()

grid = list(map(list, lines))

# right, down, left, up
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def find_grid_els(grid: list[list[str]], el: str) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    for ii, i in enumerate(grid):
        for jj, j in enumerate(i):
            if j == el:
                results.append((ii, jj))
    return results


def in_grid(r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def print_grid():
    for row in grid:
        print("".join(row))


designs = list(map(lambda x: x.strip(), lines[0].split(",")))


# def find_design_rec(des: str) -> bool:
#     if len(des) == 0:
#         return True
#     for d in designs:
#         if des.startswith(d):
#             if find_design_rec(des[len(d) :]):
#                 return True
#     return False
#
#
# print(designs)
# total = 0
# for line in lines[2:]:
#     if find_design_rec(line):
#         total += 1
# print(total)


@lru_cache(maxsize=None)
def find_design_rec(des: str) -> int:
    if len(des) == 0:
        return 1
    total = 0
    for d in designs:
        if des.startswith(d):
            res = find_design_rec(des[len(d) :])
            total += res
    return total


print(designs)
total = 0
for line in lines[2:]:
    res = find_design_rec(line)
    print(res)
    total += res
print(total)
