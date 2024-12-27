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


# def flood_fill(grid: list[list[str]], r: int, c: int):
#     fill_el = grid[r][c]
#     queue = [(r, c)]
#     visited = set()
#     visited.add((r, c))
#     perimeter = 0
#     while len(queue) > 0:
#         el = queue.pop(0)
#         for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
#             nr, nc = el[0] + dr, el[1] + dc
#             if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]):
#                 perimeter += 1
#                 continue
#             if grid[nr][nc] == fill_el:
#                 if (nr, nc) not in visited:
#                     visited.add((nr, nc))
#                     queue.append((nr, nc))
#                     continue
#             else:
#                 perimeter += 1
#     return (len(visited), perimeter, visited)
def flood_fill(grid: list[list[str]], r: int, c: int):
    fill_el = grid[r][c]
    queue = [(r, c)]
    visited = set()
    visited.add((r, c))
    # 0: left, 1: up, 2: right, 3: down
    perimeters = set()
    while len(queue) > 0:
        el = queue.pop(0)
        for dir, (dr, dc) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            nr, nc = el[0] + dr, el[1] + dc
            if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]):
                perimeters.add((dir, nr, nc))
                continue
            if grid[nr][nc] == fill_el:
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    continue
            else:
                perimeters.add((dir, nr, nc))
    deleted = set()
    for dir, r, c in perimeters:
        if (dir, r, c) in deleted:
            continue
        if dir == 0 or dir == 2:
            for j in range(r + 1, len(grid)):
                if (dir, j, c) in perimeters:
                    deleted.add((dir, j, c))
                else:
                    break
            for j in range(r - 1, -1, -1):
                if (dir, j, c) in perimeters:
                    deleted.add((dir, j, c))
                else:
                    break
        else:
            for j in range(c + 1, len(grid[0])):
                if (dir, r, j) in perimeters:
                    deleted.add((dir, r, j))
                else:
                    break
            for j in range(c - 1, -1, -1):
                if (dir, r, j) in perimeters:
                    deleted.add((dir, r, j))
                else:
                    break
    per = len(perimeters) - len(deleted)
    return (len(visited), per, visited)


visited = set()
total = 0
for ii, i in enumerate(grid):
    for jj, j in enumerate(i):
        if (ii, jj) in visited:
            continue
        area, perimeter, vis = flood_fill(grid, ii, jj)
        for v in vis:
            visited.add(v)
        print(ii, jj, area, perimeter, grid[ii][jj])
        total += area * perimeter
print(total)
