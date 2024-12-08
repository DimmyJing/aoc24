import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

grid = list(map(list, lines))

guard_pos = (-1, -1)
for ii, i in enumerate(grid):
    for jj, j in enumerate(i):
        if j == "^":
            guard_pos = (ii, jj)
print(guard_pos)
grid[guard_pos[0]][guard_pos[1]] = "X"

def has_cycle(grid: list[list[str]], guard_pos: tuple[int, int]) -> bool:
    # 0: up, 1: right, 2: down, 3: left
    dir = 0
    visited = set()
    while True:
        x, y = guard_pos
        grid[guard_pos[0]][guard_pos[1]] = "X"
        new_x, new_y = x, y
        if dir == 0:
            new_x -= 1
        elif dir == 1:
            new_y += 1
        elif dir == 2:
            new_x += 1
        elif dir == 3:
            new_y -= 1
        if new_x < 0 or new_x >= len(grid) or new_y < 0 or new_y >= len(grid[0]):
            break
        if (new_x, new_y, dir) in visited:
            return True
        visited.add((new_x, new_y, dir))
        if grid[new_x][new_y] == "." or grid[new_x][new_y] == "X":
            guard_pos = (new_x, new_y)
            continue
        elif grid[new_x][new_y] == "#":
            dir = (dir + 1) % 4
            continue
        else:
            print("impossible")
    return False

def clone_grid(grid: list[list[str]]) -> list[list[str]]:
    return [list(i) for i in grid]

total = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if i == guard_pos[0] and j == guard_pos[1]:
            continue
        new_grid = clone_grid(grid)
        new_grid[i][j] = '#'
        if has_cycle(new_grid, guard_pos):
            print(i, j)
            total += 1
print(total)
# print(grid)
# total = 0
# for line in grid:
#     for i in line:
#         if i == "X":
#             total += 1
#     print("".join(line))
# print(total)
