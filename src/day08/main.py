import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

grid = list(map(list, lines))


def print_grid(grid: list[list[str]]):
    for row in grid:
        print("".join(row))


print_grid(grid)

nodes = set()
for i in grid:
    for j in i:
        nodes.add(j)
nodes = [i for i in nodes if i != "."]
print(nodes)

# total = 0
# asdf = set()
# for node in nodes:
#     positions = []
#     for ii, i in enumerate(grid):
#         for jj, j in enumerate(i):
#             if j == node:
#                 positions.append((ii, jj))
#     for ir, ic in positions:
#         for jr, jc in positions:
#             if ir == jr and ic == jc:
#                 continue
#             new_i = ir - (ir - jr) - (ir - jr)
#             new_j = ic - (ic - jc) - (ic - jc)
#             if new_i < 0 or new_i >= len(grid) or new_j < 0 or new_j >= len(grid[0]):
#                 continue
#             # new_i = (new_i + len(grid)) % len(grid)
#             # new_j = (new_j + len(grid[0])) % len(grid[0])
#             asdf.add((new_i, new_j))
#             if grid[new_i][new_j] == ".":
#                 grid[new_i][new_j] = "#"
#     print(node, positions)
# print(len(asdf))
total = 0
asdf = set()
for node in nodes:
    positions = []
    for ii, i in enumerate(grid):
        for jj, j in enumerate(i):
            if j == node:
                positions.append((ii, jj))
    for ir, ic in positions:
        for jr, jc in positions:
            if ir == jr and ic == jc:
                continue
            new_i = ir
            new_j = ic
            while True:
                new_i = new_i - (ir - jr)
                new_j = new_j - (ic - jc)
                if new_i < 0 or new_i >= len(grid) or new_j < 0 or new_j >= len(grid[0]):
                    break
                # new_i = (new_i + len(grid)) % len(grid)
                # new_j = (new_j + len(grid[0])) % len(grid[0])
                asdf.add((new_i, new_j))
                if grid[new_i][new_j] == ".":
                    grid[new_i][new_j] = "#"
    print(node, positions)
print(len(asdf))

print_grid(grid)
# total = 0
# for i in grid:
#     for j in i:
#         if j == '#':
#             total += 1
#             pass
#
