import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)


def good_top_right(grid, i, j):
    if grid[i][j] != "A":
        return False
    new_i = i + 1
    new_j = j + 1
    if new_i < 0 or new_j < 0 or new_i >= len(grid) or new_j >= len(grid[0]):
        return False
    v1 = grid[new_i][new_j]
    new_i = i - 1
    new_j = j - 1
    if new_i < 0 or new_j < 0 or new_i >= len(grid) or new_j >= len(grid[0]):
        return False
    v2 = grid[new_i][new_j]
    if (v1 == 'M' and v2 == 'S') or (v2 == 'M' and v1 == 'S'):
        return True
    return False


def good_top_left(grid, i, j):
    if grid[i][j] != "A":
        return False
    new_i = i + 1
    new_j = j - 1
    if new_i < 0 or new_j < 0 or new_i >= len(grid) or new_j >= len(grid[0]):
        return False
    v1 = grid[new_i][new_j]
    new_i = i - 1
    new_j = j + 1
    if new_i < 0 or new_j < 0 or new_i >= len(grid) or new_j >= len(grid[0]):
        return False
    v2 = grid[new_i][new_j]
    if (v1 == 'M' and v2 == 'S') or (v2 == 'M' and v1 == 'S'):
        return True
    return False


def good_dir(grid, i, j, di, dj):
    # print(grid, i, j, di, dj)
    if grid[i][j] != "X":
        return False
    new_i = i + di
    new_j = j + dj
    if (
        new_i < 0
        or new_j < 0
        or new_i >= len(grid)
        or new_j >= len(grid[0])
        or grid[new_i][new_j] != "M"
    ):
        return False
    new_i = new_i + di
    new_j = new_j + dj
    if (
        new_i < 0
        or new_j < 0
        or new_i >= len(grid)
        or new_j >= len(grid[0])
        or grid[new_i][new_j] != "A"
    ):
        return False
    new_i = new_i + di
    new_j = new_j + dj
    if (
        new_i < 0
        or new_j < 0
        or new_i >= len(grid)
        or new_j >= len(grid[0])
        or grid[new_i][new_j] != "S"
    ):
        return False
    return True


def good(grid, i, j):
    if good_top_left(grid, i, j) and good_top_right(grid, i, j):
        return 1
    return 0
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            if good_top_left(grid, i, j) and good_top_right(grid, i, j):
                count += 1
    return count


total = 0
for i in range(len(lines)):
    for j in range(len(lines[0])):
        total += good(lines, i, j)
print(total)
