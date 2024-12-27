import copy
import re
import sys
import time
from collections import Counter
from functools import lru_cache

import networkx as nx

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

graph = nx.DiGraph()

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


grids = []
current_grid = []


# true: key, false: lock
def parse_grid(grid: list[str]) -> tuple[list[int], bool]:
    res: list[int] = []
    if grid[0][0] == "#":
        for i in range(len(grid[0])):
            for j in range(len(grid)):
                if grid[j][i] != "#":
                    res.append(j - 1)
                    break
            if grid[-1][i] == "#":
                res.append(len(grid) - 1)
    else:
        for i in range(len(grid[0])):
            for j in range(len(grid) - 1, -1, -1):
                if grid[j][i] != "#":
                    res.append(len(grid) - j - 2)
                    break
            if grid[0][i] == "#":
                res.append(len(grid) - 1)
    return res, grid[0][0] == "#"


for line in lines:
    if line == "":
        grids.append(current_grid)
        current_grid = []
    else:
        current_grid.append(list(line))
grids.append(current_grid)

print(grids)

for i in grids:
    for j in i:
        for k in j:
            print(k, end="")
        print()
    print()

keys = []
locks = []
for i in range(len(grids)):
    heights, is_key = parse_grid(grids[i])
    if is_key:
        keys.append(heights)
    else:
        locks.append(heights)

print(keys)
print(locks)
total = 0
for ii, i in enumerate(keys):
    for jj, j in enumerate(locks):
        print(ii, jj)
        good = True
        for k, l in zip(i, j):
            print("keylock", (k, l))
            if k + l >= 6:
                good = False
                break
        if good:
            total += 1
print(total)
