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


# grid = []
# for line in lines_iter:
#     if line == "":
#         break
#     grid.append(list(line))
# print_grid()
# moves = []
# for line in lines_iter:
#     for i in list(line):
#         moves.append(i)
# print(moves)
#
# pos = find_grid_els(grid, "@")[0]
#
# for move in moves:
#     if grid[pos[0]][pos[1]] != "@":
#         raise ValueError(f"Invalid pos {pos}")
#
#     dir = (0, 0)
#     if move == "^":
#         dir = (-1, 0)
#     elif move == ">":
#         dir = (0, 1)
#     elif move == "v":
#         dir = (1, 0)
#     elif move == "<":
#         dir = (0, -1)
#     else:
#         raise ValueError(f"Invalid move {move}")
#
#     new_pos = (pos[0] + dir[0], pos[1] + dir[1])
#     orig_new_pos = new_pos
#     if grid[new_pos[0]][new_pos[1]] == '.':
#         grid[orig_new_pos[0]][orig_new_pos[1]] = "@"
#         grid[pos[0]][pos[1]] = "."
#         pos = orig_new_pos
#     else:
#         while grid[new_pos[0]][new_pos[1]] == "O":
#             new_pos = (new_pos[0] + dir[0], new_pos[1] + dir[1])
#         if grid[new_pos[0]][new_pos[1]] == '#':
#             pass
#         elif grid[new_pos[0]][new_pos[1]] == '.':
#             # print(pos)
#             # print(orig_new_pos)
#             # print(new_pos)
#             grid[orig_new_pos[0]][orig_new_pos[1]] = "@"
#             grid[pos[0]][pos[1]] = "."
#             grid[new_pos[0]][new_pos[1]] = 'O'
#             pos = orig_new_pos
#     # print_grid()
#
# total = 0
# for ii, i in enumerate(grid):
#     for jj, j in enumerate(i):
#         if j == 'O':
#             total += ii * 100 + jj
# print_grid()
# print(total)
grid = []
for line in lines_iter:
    if line == "":
        break
    grid.append([])
    for i in line:
        if i == "#":
            grid[-1].append("#")
            grid[-1].append("#")
        elif i == "O":
            grid[-1].append("[")
            grid[-1].append("]")
        elif i == ".":
            grid[-1].append(".")
            grid[-1].append(".")
        elif i == "@":
            grid[-1].append("@")
            grid[-1].append(".")
print_grid()
moves = []
for line in lines_iter:
    for i in list(line):
        moves.append(i)


print(moves)

pos = find_grid_els(grid, "@")[0]


def can_move_recursive(
    pos: tuple[int, int], up: bool, affected: set[tuple[int, int]]
) -> bool:
    affected.add(pos)
    affected.add((pos[0], pos[1] + 1))
    new_pos_1 = (pos[0] - 1, pos[1])
    new_pos_2 = (pos[0] - 1, pos[1] + 1)
    if not up:
        new_pos_1 = (pos[0] + 1, pos[1])
        new_pos_2 = (pos[0] + 1, pos[1] + 1)
    if grid[new_pos_1[0]][new_pos_1[1]] == "#":
        return False
    if grid[new_pos_2[0]][new_pos_2[1]] == "#":
        return False
    if grid[new_pos_1[0]][new_pos_1[1]] == "[":
        return can_move_recursive(new_pos_1, up, affected)
    if grid[new_pos_1[0]][new_pos_1[1]] == "]":
        if not can_move_recursive((new_pos_1[0], new_pos_1[1] - 1), up, affected):
            return False
    if grid[new_pos_2[0]][new_pos_2[1]] == "[":
        if not can_move_recursive(new_pos_2, up, affected):
            return False
    return True


def move_recursive(pos: tuple[int, int], up: bool):
    new_pos_1 = (pos[0] - 1, pos[1])
    new_pos_2 = (pos[0] - 1, pos[1] + 1)
    if not up:
        new_pos_1 = (pos[0] + 1, pos[1])
        new_pos_2 = (pos[0] + 1, pos[1] + 1)
    if grid[new_pos_1[0]][new_pos_1[1]] == "[":
        move_recursive(new_pos_1, up)
    if grid[new_pos_1[0]][new_pos_1[1]] == "]":
        move_recursive((new_pos_1[0], new_pos_1[1] - 1), up)
    if grid[new_pos_2[0]][new_pos_2[1]] == "[":
        move_recursive(new_pos_2, up)
    grid[new_pos_1[0]][new_pos_1[1]] = "["
    grid[new_pos_2[0]][new_pos_2[1]] = "]"
    grid[pos[0]][pos[1]] = "."
    grid[pos[0]][pos[1] + 1] = "."


for move in moves:
    if grid[pos[0]][pos[1]] != "@":
        raise ValueError(f"Invalid pos {pos}")

    dir = (0, 0)
    if move == "^":
        dir = (-1, 0)
    elif move == ">":
        dir = (0, 1)
    elif move == "v":
        dir = (1, 0)
    elif move == "<":
        dir = (0, -1)
    else:
        raise ValueError(f"Invalid move {move}")

    new_pos = (pos[0] + dir[0], pos[1] + dir[1])
    orig_new_pos = new_pos
    if grid[new_pos[0]][new_pos[1]] == ".":
        grid[orig_new_pos[0]][orig_new_pos[1]] = "@"
        grid[pos[0]][pos[1]] = "."
        pos = orig_new_pos
    elif dir[0] == 0:
        while (
            grid[new_pos[0]][new_pos[1]] == "[" or grid[new_pos[0]][new_pos[1]] == "]"
        ):
            new_pos = (new_pos[0] + dir[0], new_pos[1] + dir[1])
        if grid[new_pos[0]][new_pos[1]] == "#":
            pass
        elif grid[new_pos[0]][new_pos[1]] == ".":
            for i in range(new_pos[1], pos[1], -dir[1]):
                grid[pos[0]][i] = grid[pos[0]][i - dir[1]]
            grid[pos[0]][pos[1]] = "."
            pos = orig_new_pos
    else:
        up = dir[0] == -1
        affected = set()
        can_move = False
        if grid[orig_new_pos[0]][orig_new_pos[1]] == "[":
            can_move = can_move_recursive(orig_new_pos, up, affected)
        elif grid[orig_new_pos[0]][orig_new_pos[1]] == "]":
            can_move = can_move_recursive(
                (orig_new_pos[0], orig_new_pos[1] - 1), up, affected
            )
        if not can_move:
            pass
        else:
            if grid[orig_new_pos[0]][orig_new_pos[1]] == "[":
                move_recursive(orig_new_pos, up)
            elif grid[orig_new_pos[0]][orig_new_pos[1]] == "]":
                move_recursive((orig_new_pos[0], orig_new_pos[1] - 1), up)
            grid[pos[0]][pos[1]] = "."
            pos = orig_new_pos
            grid[pos[0]][pos[1]] = "@"
            if grid[pos[0]][pos[1] + 1] == "]":
                grid[pos[0]][pos[1] + 1] = "."
            elif grid[pos[0]][pos[1] - 1] == "[":
                grid[pos[0]][pos[1] - 1] = "."
    print(move)
    print_grid()

total = 0
for ii, i in enumerate(grid):
    for jj, j in enumerate(i):
        if j == "[":
            total += ii * 100 + jj
print_grid()
print(total)
