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

graph = nx.Graph(create_using=nx.DiGraph)

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


adj_list = {}


# sets: set[tuple[str, str, str]] = set()
# for line in lines:
#     a, b = line.split("-")
#     if a not in adj_list:
#         adj_list[a] = []
#     if b not in adj_list:
#         adj_list[b] = []
#     adj_list[a].append(b)
#     adj_list[b].append(a)
#
# for i in adj_list:
#     for j in adj_list:
#         for k in adj_list:
#             if i == j or j == k or i == k:
#                 continue
#             if j not in adj_list[i] or k not in adj_list[i]:
#                 continue
#             if i not in adj_list[j] or k not in adj_list[j]:
#                 continue
#             if i not in adj_list[k] or j not in adj_list[k]:
#                 continue
#             sets.add(tuple(sorted([i, j, k])))
# print(sets)
#
# total = 0
# for a, b, c in iter(sets):
#     if a[0] == "t" or b[0] == "t" or c[0] == "t":
#         total += 1
# print(total)
sets: set[tuple[str, str, str]] = set()
nodes: set[str] = set()
for line in lines:
    a, b = line.split("-")
    if a not in nodes:
        nodes.add(a)
        graph.add_node(a)
    if b not in nodes:
        nodes.add(b)
        graph.add_node(b)
    graph.add_edge(a, b)
    graph.add_edge(b, a)

longest = 0
longest_path = []
for c in nx.enumerate_all_cliques(graph):
    if len(c) > longest:
        longest = len(c)
        longest_path = c
print(",".join(sorted(longest_path)))
