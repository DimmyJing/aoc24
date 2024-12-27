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

graph = nx.Graph()

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


coords = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}
dir_coords = {
    0: (1, 2),
    1: (1, 1),
    2: (1, 0),
    3: (0, 1),
    4: (0, 2),
}
reverse_dir_map = {0: ">", 1: "v", 2: "<", 3: "^", 4: "A"}


# def find_path_1(letters: str) -> list[list[int]]:
#     paths = []
#     current_coord = (3, 2)
#     for letter in letters:
#         path1 = []
#         path2 = []
#         coord = coords[letter]
#         res = []
#         if coord[0] > current_coord[0]:
#             for _ in range(current_coord[0], coord[0]):
#                 res.append(1)
#         elif coord[0] < current_coord[0]:
#             for _ in range(coord[0], current_coord[0]):
#                 res.append(3)
#         if coord[1] > current_coord[1]:
#             for _ in range(current_coord[1], coord[1]):
#                 res.append(0)
#         elif coord[1] < current_coord[1]:
#             for _ in range(coord[1], current_coord[1]):
#                 res.append(2)
#
#         if coord[0] == 3 and current_coord[1] == 0:
#             path1.extend(reversed(res))
#             path2.extend(reversed(res))
#         elif coord[1] == 0 and current_coord[0] == 3:
#             path1.extend(res)
#             path2.extend(res)
#         else:
#             path1.extend(res)
#             path2.extend(reversed(res))
#         path1.append(4)
#         path2.append(4)
#         current_coord = coord
#         new_paths = []
#         if len(paths) == 0:
#             new_paths.append(path1)
#             new_paths.append(path2)
#         else:
#             for path in paths:
#                 new_paths.append(path + path1)
#                 new_paths.append(path + path2)
#         paths = new_paths
#     return paths
#
#
# def find_path_2(letters: list[int]) -> list[list[int]]:
#     paths = []
#     current_coord = (0, 2)
#     for ll, letter in enumerate(letters):
#         path1 = []
#         path2 = []
#         coord = dir_coords[letter]
#         res = []
#         if coord[0] > current_coord[0]:
#             for _ in range(current_coord[0], coord[0]):
#                 res.append(1)
#         elif coord[0] < current_coord[0]:
#             for _ in range(coord[0], current_coord[0]):
#                 res.append(3)
#         if coord[1] > current_coord[1]:
#             for _ in range(current_coord[1], coord[1]):
#                 res.append(0)
#         elif coord[1] < current_coord[1]:
#             for _ in range(coord[1], current_coord[1]):
#                 res.append(2)
#         if coord[0] == 0 and current_coord[1] == 0:
#             path1.extend(reversed(res))
#             path2.extend(reversed(res))
#         elif coord[1] == 0 and current_coord[0] == 0:
#             path1.extend(res)
#             path2.extend(res)
#         else:
#             path1.extend(res)
#             path2.extend(reversed(res))
#         path1.append(4)
#         path2.append(4)
#         current_coord = coord
#         new_paths = []
#         if len(paths) == 0:
#             new_paths.append(path1)
#             new_paths.append(path2)
#         else:
#             for path in paths:
#                 new_paths.append(path + path1)
#                 new_paths.append(path + path2)
#         paths = new_paths
#         paths = list(map(list, list(set(map(tuple, paths)))))
#     return paths
#
#
# def print_path(path: list[int]):
#     for i in path:
#         print(reverse_dir_map[i], end="")
#     print()
#
#
# def find_paths_2(paths: list[list[int]]):
#     result = []
#     for path in paths:
#         result.extend(find_path_2(path))
#     result = list(set(map(tuple, result)))
#     return result
#
#
# total = 0
# for line in lines:
#     aaaa = int(line[:-1])
#     paths = find_path_1(line)
#     paths = list(set(map(tuple, paths)))
#     for i in range(25):
#         print(f"finding paths {i} {len(paths)}")
#         paths = find_paths_2(paths)
#     min_seq = (None, None)
#     for ii, i in enumerate(paths):
#         if min_seq[0] is (None) or len(i) < len(min_seq[0]):
#             min_seq = (i, ii)
#     # print_path(min_seq[0])
#     # print(min_seq[1])
#     # print(len(min_seq[0]))
#     # print(aaaa)
#     print(aaaa, len(min_seq[0]))
#     total += aaaa * len(min_seq[0])
# print(total)

num_2 = 25
path_2_dp: list[dict[tuple[int, int, int, int], int]] = [{} for _ in range(num_2)]


def find_paths_1_rec(
    sr: int, sc: int, dr: int, dc: int, visited: set[tuple[int, int]]
) -> list[list[int]]:
    if sr == dr and sc == dc:
        return [[]]
    paths = []
    visited.add((sr, sc))
    for dd, d in enumerate(dirs):
        nr = sr + d[0]
        nc = sc + d[1]
        if not (0 <= nr < 4 and 0 <= nc < 3 and (nr != 3 or nc != 0)):
            continue
        if (nr, nc) in visited:
            continue
        res = find_paths_1_rec(nr, nc, dr, dc, visited)
        for i in res:
            paths.append([dd] + i)
    visited.remove((sr, sc))
    return paths


def find_paths_1(sr: int, sc: int, dr: int, dc: int) -> list[list[int]]:
    visited = set()
    paths = find_paths_1_rec(sr, sc, dr, dc, visited)
    return paths


def find_paths_2_rec(
    sr: int, sc: int, dr: int, dc: int, visited: set[tuple[int, int]]
) -> list[list[int]]:
    if sr == dr and sc == dc:
        return [[]]
    paths = []
    visited.add((sr, sc))
    for dd, d in enumerate(dirs):
        nr = sr + d[0]
        nc = sc + d[1]
        if not (0 <= nr < 2 and 0 <= nc < 3 and (nr != 0 or nc != 0)):
            continue
        if (nr, nc) in visited:
            continue
        res = find_paths_2_rec(nr, nc, dr, dc, visited)
        for i in res:
            paths.append([dd] + i)
    visited.remove((sr, sc))
    return paths


def find_paths_2(sr: int, sc: int, dr: int, dc: int) -> list[list[int]]:
    visited = set()
    paths = find_paths_2_rec(sr, sc, dr, dc, visited)
    # print((sr, sc), (dr, dc), paths)
    return paths


def get_path_len(path: list[int], depth: int) -> int:
    # if path == [0]:
    #     print("hi=====================")
    # print("path", path)
    current_pos = (0, 2)
    total_len = 0
    for p in path:
        new_pos = dir_coords[p]
        dp_idx = (current_pos[0], current_pos[1], new_pos[0], new_pos[1])
        dp_len = path_2_dp[depth + 1][dp_idx]
        total_len += dp_len
        current_pos = new_pos
        # print(dp_idx, dp_len)

    new_pos = dir_coords[4]
    dp_idx = (current_pos[0], current_pos[1], new_pos[0], new_pos[1])
    dp_len = path_2_dp[depth + 1][dp_idx]
    total_len += dp_len
    # print(dp_idx, dp_len)
    # if path == [0]:
    #     print("hi=====================")

    return total_len


for i in range(num_2 - 1, -1, -1):
    for ii in range(2):
        for jj in range(3):
            for kk in range(2):
                for ll in range(3):
                    if (ii == 0 and jj == 0) or (kk == 0 and ll == 0):
                        continue
                    dp_array = path_2_dp[i]
                    if i == num_2 - 1:
                        dp_array[(ii, jj, kk, ll)] = abs(ii - kk) + abs(jj - ll) + 1
                        continue
                    paths = find_paths_2(ii, jj, kk, ll)
                    path_lens = list(map(lambda x: get_path_len(x, i), paths))
                    dp_array[(ii, jj, kk, ll)] = min(path_lens)


total = 0
for line in lines:
    coord = coords["A"]
    aaaa = int(line[:-1])
    result = 0
    for l in line:
        new_coord = coords[l]
        paths = find_paths_1(coord[0], coord[1], new_coord[0], new_coord[1])
        path_lens = list(map(lambda x: get_path_len(x, -1), paths))
        result += min(path_lens)
        coord = new_coord
    total += aaaa * result
    print(result)
print(total)
# path = [2, 4, 3, 4, 0, 3, 3, 4, 1, 1, 1, 4]
# print("alwijdaiwjdalwidjaliwdjlaijdliwjdliwjd")
# path_len = get_path_len(path, -1) - 1
# print(path_len)
# print(path_2_dp[0])
