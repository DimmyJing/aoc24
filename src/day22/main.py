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


def prune(n: int) -> int:
    return n % 16777216


def mix(a: int, b: int) -> int:
    return a ^ b


def process(n: int):
    a = prune(mix(n, n * 64))
    b = prune(mix(a, a // 32))
    c = prune(mix(b, b * 2048))
    return c


# total = 0
# for line in lines:
#     line = int(line)
#     for i in range(2000):
#         line = process(line)
#     total += line
#     print(line)
# print(total)

sequences: list[list[int]] = []

seq_sums: list[dict[tuple[int, int, int, int], int]] = []

for line in lines:
    line = int(line)
    sequences.append([line % 10])
    for i in range(2000):
        line = process(line)
        sequences[-1].append(line % 10)

    sequence = sequences[-1]
    seq_diffs = [i - j for i, j in zip(sequence[1:], sequence[:-1])]

    seq_sum: dict[tuple[int, int, int, int], int] = {}
    for i in range(3, len(seq_diffs)):
        key: tuple[int, int, int, int] = (
            seq_diffs[i - 3],
            seq_diffs[i - 2],
            seq_diffs[i - 1],
            seq_diffs[i],
        )
        val = sequence[i + 1]
        if key not in seq_sum:
            seq_sum[key] = val

    seq_sums.append(seq_sum)

max_sum = 0
max_key = None
for i in range(-9, 10):
    for j in range(-9, 10):
        print(i, j)
        for k in range(-9, 10):
            for l in range(-9, 10):
                # print(i, j, k, l)
                total = 0
                for seq_sum in seq_sums:
                    if (i, j, k, l) in seq_sum:
                        total += seq_sum[(i, j, k, l)]
                if total > max_sum:
                    max_sum = total
                    max_key = (i, j, k, l)
print(max_key)
print(max_sum)
