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


grid_r = 103
grid_c = 101
# grid_r = 7
# grid_c = 11

# positions = []
#
# for line in lines:
#     _, p, v = line.split("=")
#     pr, pc = p.split(",")
#     pc = pc.split(" ")[0]
#     vr, vc = v.split(",")
#     vc = vc.split(" ")[0]
#     pr, pc = int(pr), int(pc)
#     vr, vc = int(vr), int(vc)
#     pr, pc = pc, pr
#     vr, vc = vc, vr
#     print(pr, pc, vr, vc)
#     new_r = (pr + (100 * vr) + (grid_r * (10**5))) % grid_r
#     new_c = (pc + (100 * vc) + (grid_c * (10**5))) % grid_c
#     positions.append((new_r, new_c))
#
# topleft = 0
# topright = 0
# bottomleft = 0
# bottomright = 0
# new_grid = [[None] * grid_c for _ in range(grid_r)]
# for r, c in positions:
#     print((r, c))
#     if new_grid[r][c] is None:
#         new_grid[r][c] = 1
#     else:
#         new_grid[r][c] += 1
#     print(r, c)
#     top = r < grid_r // 2
#     bottom = r > grid_r // 2
#     left = c < grid_c // 2
#     right = c > grid_c // 2
#     if top and left:
#         topleft += 1
#     elif top and right:
#         topright += 1
#     elif bottom and left:
#         bottomleft += 1
#     elif bottom and right:
#         bottomright += 1
# for row in new_grid:
#     for col in row:
#         if col is None:
#             print(".", end="")
#         else:
#             print(col, end="")
#     print()
# print(topleft, topright, bottomleft, bottomright)
# print(topleft * topright * bottomleft * bottomright)
positions = []

for line in lines:
    _, p, v = line.split("=")
    pr, pc = p.split(",")
    pc = pc.split(" ")[0]
    vr, vc = v.split(",")
    vc = vc.split(" ")[0]
    pr, pc = int(pr), int(pc)
    vr, vc = int(vr), int(vc)
    pr, pc = pc, pr
    vr, vc = vc, vr
    print(pr, pc, vr, vc)
    new_r = (pr + (100 * vr) + (grid_r * (10**5))) % grid_r
    new_c = (pc + (100 * vc) + (grid_c * (10**5))) % grid_c
    positions.append((pr, pc, vr, vc))


def get_position_sec(
    positions: list[tuple[int, int, int, int]], sec: int
) -> list[tuple[int, int]]:
    new_positions = []
    for r, c, vr, vc in positions:
        new_r = (r + (sec * vr) + (grid_r * (10**7))) % grid_r
        new_c = (c + (sec * vc) + (grid_c * (10**7))) % grid_c
        new_positions.append((new_r, new_c))
    return new_positions


def print_positions(positions: list[tuple[int, int]]):
    num_connected = 0

    new_grid: list[list[int | None]] = [[None] * grid_c for _ in range(grid_r)]
    for r, c in positions:
        if new_grid[r][c] is None:
            new_grid[r][c] = 1
        else:
            new_grid[r][c] += 1
    num_set = 0
    for rr, r in enumerate(new_grid):
        for cc, c in enumerate(r):
            if c is not None:
                num_set += 1
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if 0 <= rr + dr < grid_r and 0 <= cc + dc < grid_c:
                        if new_grid[rr + dr][cc + dc] is not None:
                            num_connected += 1
                            break
    if num_connected / num_set > 0.4:
        for row in new_grid:
            for col in row:
                if col is None:
                    print(".", end="")
                else:
                    print(col, end="")
            print()
        time.sleep(1)


for i in range(100000):
    print_positions(get_position_sec(positions, i))
    print("seconds", i)
    # time.sleep(0.1)
