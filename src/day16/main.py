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


start = find_grid_els(grid, "S")[0]
end = find_grid_els(grid, "E")[0]

grid[end[0]][end[1]] = "."
grid[start[0]][start[1]] = "."

grid_cost = [[[-1] * 4 for _ in range(len(grid[0]))] for _ in range(len(grid))]
grid_cost[start[0]][start[1]][0] = 0

# 0 - right, 1 - down, 2 - left, 3 - up
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

queue = [(start, 0)]

visited = set()

while len(queue) > 0:
    (r, c), dir = queue.pop(0)
    print(f"visiting {r} {c} {dir}")
    visited.add((r, c, dir))
    old_cost = grid_cost[r][c][dir]
    new_r, new_c = r + dirs[dir][0], c + dirs[dir][1]
    if (
        0 <= new_r < len(grid)
        and 0 <= new_c < len(grid[0])
        and grid[new_r][new_c] != "#"
    ):
        cost = grid_cost[new_r][new_c][dir]
        print("cost", cost, new_r, new_c, dir)
        if cost == -1 or old_cost + 1 < cost:
            print(f"a going to {new_r} {new_c} {dir} with cost {old_cost + 1}")
            grid_cost[new_r][new_c][dir] = old_cost + 1
            queue.append(((new_r, new_c), dir))
    for i in [-1, 1]:
        new_dir = (dir + i + 4) % 4
        new_r, new_c = r + dirs[new_dir][0], c + dirs[new_dir][1]
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and grid[new_r][new_c] != "#"
        ):
            cost = grid_cost[new_r][new_c][new_dir]
            if cost == -1 or old_cost + 1001 < cost:
                print(
                    f"b going to {new_r} {new_c} {new_dir} with cost {old_cost + 1001}"
                )
                grid_cost[new_r][new_c][new_dir] = old_cost + 1001
                queue.append(((new_r, new_c), new_dir))
final_dirs = []
total = float("inf")
for ii, i in enumerate(grid_cost[end[0]][end[1]]):
    if i != -1 and i < total:
        total = i
        final_dirs = [ii]
    elif i != -1 and i == total:
        final_dirs.append(ii)


def find_best_path(
    grid_cost: list[list[list[int]]],
    r: int,
    c: int,
    dir: int,
    visited: set[tuple[int, int, int]],
):
    visited.add((r, c, dir))
    current_cost = grid_cost[r][c][dir]
    back = dirs[(dir + 2) % 4]
    new_r, new_c = r + back[0], c + back[1]
    if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
        new_cost = grid_cost[new_r][new_c][dir]
        if new_cost == current_cost - 1:
            find_best_path(grid_cost, new_r, new_c, dir, visited)
        for i in [-1, 1]:
            new_dir = (dir + i + 4) % 4
            new_cost = grid_cost[new_r][new_c][new_dir]
            if new_cost == current_cost - 1001:
                find_best_path(grid_cost, new_r, new_c, new_dir, visited)


visited = set()
for dir in final_dirs:
    find_best_path(grid_cost, end[0], end[1], dir, visited)


asdf = 0
for i in visited:
    if grid[i[0]][i[1]] == ".":
        asdf += 1
        grid[i[0]][i[1]] = "X"
print_grid()

print(total)
print(len(visited))
print(asdf)
