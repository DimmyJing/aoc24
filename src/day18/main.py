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


# grid_size = 7
grid_size = 71

falling_bytes = []


for line in lines:
    x, y = map(int, line.split(","))
    # r, c
    falling_bytes.append((y, x))


def find_path_rec(distances, r, c) -> set[tuple[int, int]]:
    dist = distances[r][c]
    if dist == 0:
        res = set()
        res.add((r, c))
        return res
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if (
            0 <= nr < grid_size
            and 0 <= nc < grid_size
            and distances[nr][nc] == dist - 1
        ):
            res = find_path_rec(distances, nr, nc)
            res.add((r, c))
            return res
    return set()


# for bb, b in enumerate(falling_bytes):
#     if bb >= 1024:
#         break
#     grid[b[0]][b[1]] = "#"


def find_path(grid) -> set[tuple[int, int]]:
    distances = [[-1] * grid_size for _ in range(grid_size)]
    distances[0][0] = 0

    queue = [(0, 0)]
    while len(queue) > 0:
        r, c = queue.pop(0)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < grid_size
                and 0 <= nc < grid_size
                and grid[nr][nc] != "#"
                and distances[nr][nc] == -1
            ):
                distances[nr][nc] = distances[r][c] + 1
                queue.append((nr, nc))
    if distances[-1][-1] == -1:
        return set()
    path = find_path_rec(distances, grid_size - 1, grid_size - 1)
    return path


grid = [["."] * grid_size for _ in range(grid_size)]
path = set()
for bb, b in enumerate(falling_bytes):
    grid[b[0]][b[1]] = "#"
    print_grid()
    print()
    print()
    print()
    if len(path) == 0 or (b[0], b[1]) in path:
        path = find_path(grid)
        if (0, 0) not in path:
            print("hello world", bb, b)
            break


# print_grid()
# print(distances[-1][-1])
#
# for ii, i in enumerate(distances):
#     for jj, j in enumerate(i):
#         if j != -1:
#             grid[ii][jj] = "O"
#
# # print_grid()
