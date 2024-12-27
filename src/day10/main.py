import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

grid = list(map(list, lines))

# def num_matches(grid: list[list[str]], r: int, c: int):
#     count = 0
#     visited = set()
#     visited.add((r, c))
#     queue = [(r, c)]
#     while len(queue) > 0:
#         r, c = queue.pop(0)
#         for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             r_new, c_new = r + dr, c + dc
#             if r_new < 0 or r_new >= len(grid) or c_new < 0 or c_new >= len(grid[0]):
#                 continue
#             if grid[r_new][c_new] == '.':
#                 continue
#             if int(grid[r_new][c_new]) - int(grid[r][c]) != 1:
#                 continue
#             if (r_new, c_new) in visited:
#                 continue
#             visited.add((r_new, c_new))
#             queue.append((r_new, c_new))
#             if grid[r_new][c_new] == "9":
#                 count += 1
#     return count


def num_matches(grid: list[list[str]], r: int, c: int):
    if grid[r][c] == "9":
        return 1
    count = 0
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r_new, c_new = r + dr, c + dc
        if r_new < 0 or r_new >= len(grid) or c_new < 0 or c_new >= len(grid[0]):
            continue
        if grid[r_new][c_new] == ".":
            continue
        if int(grid[r_new][c_new]) - int(grid[r][c]) != 1:
            continue
        count += num_matches(grid, r_new, c_new)
    return count


total = 0
for rr, r in enumerate(grid):
    for cc, c in enumerate(r):
        if c == "0":
            matches = num_matches(grid, rr, cc)
            total += matches
            print(f"{rr} {cc} {matches}")
print(total)
