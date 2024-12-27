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


start_pos = find_grid_els(grid, "S")[0]
end_pos = find_grid_els(grid, "E")[0]
distances = [[-1] * len(grid[0]) for _ in range(len(grid))]
distances[start_pos[0]][start_pos[1]] = 0
queue = [start_pos]
while len(queue) > 0:
    r, c = queue.pop(0)
    dist = distances[r][c]
    for d in dirs:
        nr = r + d[0]
        nc = c + d[1]
        if in_grid(nr, nc) and grid[nr][nc] != "#":
            new_dist = distances[nr][nc]
            if new_dist != -1 and new_dist <= dist + 1:
                continue
            distances[nr][nc] = dist + 1
            queue.append((nr, nc))


# cheats = set()
# total = 0
# for r, i in enumerate(grid):
#     for c, j in enumerate(i):
#         d1 = distances[r][c]
#         if d1 == -1:
#             continue
#         for dr1, dc1 in dirs:
#             for dr2, dc2 in dirs:
#                 nr, nc = r + dr1 + dr2, c + dc1 + dc2
#                 if not in_grid(nr, nc):
#                     continue
#                 d2 = distances[nr][nc]
#                 if d1 == -1:
#                     continue
#                 cheat_time = d2 - d1 - 2
#                 if cheat_time > 0:
#                     cheats.add((r, c, nr, nc, cheat_time))
#
# print(distances[end_pos[0]][end_pos[1]])
# print(distances)
# print(total)
# print(cheats)
# for cheat in cheats:
#     if cheat[4] >= 100:
#         total += 1
#     # print("cheat", cheat[4])
# print(total)

path = [start_pos]
while path[-1] != end_pos:
    r, c = path[-1]
    dist = distances[r][c]
    for d in dirs:
        nr = r + d[0]
        nc = c + d[1]
        if in_grid(nr, nc) and distances[nr][nc] == dist + 1:
            path.append((nr, nc))
            break
print(path)

cheat = 20

total = 0
a = set()
b = []
for i, (r, c) in enumerate(path):
    print(i)
    for j in range(i + 1, len(path)):
        rr, cc = path[j]
        cheat_dist = abs(r - rr) + abs(c - cc)
        if cheat_dist > cheat:
            continue
        cheat_time = j - i - cheat_dist
        if cheat_time >= 100:
            a.add((r, c, rr, cc, cheat_time))
            b.append(cheat_time)
# print(len(path))
print(len(a))
print(Counter(b))
