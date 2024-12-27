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

graph = nx.DiGraph()

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


# node_inps: dict[str, tuple[str, str, str]] = {}
#
# nodes: set[str] = set()
# node_states: dict[str, bool] = {}
# gate = False
# for line in lines:
#     if line == "":
#         gate = True
#         continue
#     if not gate:
#         a, b = line.split(":")
#         graph.add_node(a)
#         if int(b.strip()) == 1:
#             node_states[a] = True
#         else:
#             node_states[a] = False
#     else:
#         a, b, c, _, d = line.split(" ")
#         node1 = a
#         node2 = c
#         operation = b
#         node3 = d
#
#         if node1 not in nodes:
#             graph.add_node(node1)
#             nodes.add(node1)
#         if node2 not in nodes:
#             graph.add_node(node2)
#             nodes.add(node2)
#         if node3 not in nodes:
#             graph.add_node(node3)
#             nodes.add(node3)
#
#         graph.add_edge(node1, node3)
#         graph.add_edge(node2, node3)
#         node_inps[node3] = (node1, node2, operation)
#
#
# print(len(nodes))
#
# asdf = list((nx.topological_sort(graph)))
# for node in asdf:
#     if node in node_states:
#         continue
#     node1, node2, operation = node_inps[node]
#     if operation == "AND":
#         node_states[node] = node_states[node1] and node_states[node2]
#     elif operation == "OR":
#         node_states[node] = node_states[node1] or node_states[node2]
#     elif operation == "XOR":
#         node_states[node] = node_states[node1] ^ node_states[node2]
# print(asdf)
# res = ""
# for i in range(100):
#     node = f"z{i:02d}"
#     if node in node_states:
#         if node_states[node]:
#             res = "1" + res
#         else:
#             res = "0" + res
#
# res = "0b" + res
# print(int(res, 2))


node_inps: dict[str, tuple[str, str, str]] = {}

nodes: set[str] = set()
node_states: dict[str, bool] = {}
gate = False
for line in lines:
    if line == "":
        gate = True
        continue
    if not gate:
        a, b = line.split(":")
        graph.add_node(a)
        if int(b.strip()) == 1:
            node_states[a] = True
        else:
            node_states[a] = False
    else:
        a, b, c, _, d = line.split(" ")
        node1 = a
        node2 = c
        operation = b
        node3 = d

        if node1 not in nodes:
            graph.add_node(node1)
            nodes.add(node1)
        if node2 not in nodes:
            graph.add_node(node2)
            nodes.add(node2)
        if node3 not in nodes:
            graph.add_node(node3)
            nodes.add(node3)

        graph.add_edge(node1, node3)
        graph.add_edge(node2, node3)
        node_inps[node3] = (node1, node2, operation)


# def evaluate(operations: dict[str, tuple[str, str, str]]) -> dict[str, bool]:
#     new_node_states = copy.deepcopy(node_states)
#     for node in nx.topological_sort(graph):
#         if node in new_node_states:
#             continue
#         node1, node2, operation = operations[node]
#         if operation == "AND":
#             new_node_states[node] = new_node_states[node1] and new_node_states[node2]
#         elif operation == "OR":
#             new_node_states[node] = new_node_states[node1] or new_node_states[node2]
#         elif operation == "XOR":
#             new_node_states[node] = new_node_states[node1] ^ new_node_states[node2]
#     return new_node_states


num_bits = 0
for i in range(100):
    if f"z{i:02d}" not in nodes:
        num_bits = i - 1
        break


def get_xyz(n: int) -> tuple[str, str, str]:
    return f"x{n:02d}", f"y{n:02d}", f"z{n:02d}"


# xors = list()
# ands = list()
# print(num_bits)
# for i in range(num_bits):
#     xn, yn, _ = get_xyz(i)
#     print(xn)
#     for n in nx.topological_sort(graph):
#         if n not in node_inps:
#             continue
#         (a, b, c) = node_inps[n]
#         if a == xn or b == xn:
#             if c == "XOR":
#                 xors.append(n)
#             elif c == "AND":
#                 ands.append(n)
#     assert len(xors) == i + 1
#     assert len(ands) == i + 1
#
# print(xors)
# print(ands)
#
# for i in xors:
#     if i[0] == "z" and i != "z00":
#         print(i)
# for i in ands:
#     if i[0] == "z" and i != "z00":
#         print(i)
#
# swappable = set(list(nodes))
#
# swaps: list[tuple[str, str]] = []
# if xors[0] != "z00":
#     swaps.append(("z00", xors[0]))
#     node_inps["z00"], node_inps[xors[0]] = node_inps[xors[0]], node_inps["z00"]
#     swap_el = xors[0]
#     xors[0] = "z00"
#     swappable.remove(swap_el)
# swappable.remove("z00")
#
# for i in range(1, num_bits):
#     xn, yn, zn = get_xyz(i)
#     for j in nodes:
#         if j in node_inps:
#             a, b, c = node_inps[j]
#             if (a == xors[i] or b == xors[i]) and c == "XOR":
#                 if j[0] != "z":
#                     print(i, j, c, "this is sus")
#                     swaps.append((j, zn))
#
#
# for node in nodes:
#     good = False
#     for j in nodes:
#         if j in node_inps:
#             a, b, c = node_inps[j]
#             if a == node or b == node:
#                 good = True
#     if not good:
#         if node[0] != "z":
#             print(node, "this is sus")
# for i in range(num_bits + 1):
#     _, _, zn = get_xyz(i)
#     for j in nodes:
#         if j in node_inps:
#             a, b, c = node_inps[j]
#             if a == zn or b == zn:
#                 print(i, j, c, "this is sus")
#
#
# print(swaps)
#
#
# # def test_correct(n) -> bool:
# #     xn = f"x{n:02d}"
# #     xn1 = f"x{n + 1:02d}"
# #     yn = f"y{n:02d}"
# #     yn1 = f"y{n + 1:02d}"
# #     zn = f"z{n:02d}"
# #     zn1 = f"z{n + 1:02d}"
# #     if xn not in nodes or xn1 not in nodes or yn not in nodes or yn1 not in nodes:
# #         return True
# #     for i in range(2):
# #         for j in range(2):
# #             for k in range(2):
# #                 for l in range(2):
# #                     node_states[xn] = bool(i)
# #                     node_states[yn] = bool(j)
# #                     node_states[xn1] = bool(k)
# #                     node_states[yn1] = bool(l)
# #                     res = evaluate(node_inps)
# #                     if res[zn] != (i ^ j):
# #                         return False
# #                     if res[zn1] != (k ^ l + (i and j)) % 2:
# #                         return False
# #     return True
# #
# #
# # counts = []
# # depths: dict[str, int] = {}
# # for node in nx.topological_sort(graph):
# #     if node in node_states:
# #         depths[node] = 0
# #     else:
# #         node1, node2, operation = node_inps[node]
# #         depths[node] = max(depths[node1], depths[node2]) + 1
# #
# # print(depths)
# #
# # for i in range(100):
# #     if f"z{i + 1:02d}" not in nodes:
# #         break
# #     xn = f"x{i:02d}"
# #     yn = f"y{i:02d}"
# #     counts.append(0)
# #     has_and = False
# #     has_xor = False
# #     for n in nx.topological_sort(graph):
# #         if n not in node_inps:
# #             continue
# #         (a, b, c) = node_inps[n]
# #         if a == xn or b == xn:
# #             print(f"Found {xn} {c} {a if a != xn else b}")
# #             counts[-1] += 1
# #             if c == "AND":
# #                 if has_and:
# #                     print("AND")
# #                 has_and = True
# #             elif c == "XOR":
# #                 if has_xor:
# #                     print("XOR")
# #                 has_xor = True
# #     counts.append(0)
# #     has_and = False
# #     has_xor = False
# #     for n in nx.topological_sort(graph):
# #         if n not in node_inps:
# #             continue
# #         (a, b, c) = node_inps[n]
# #         if a == yn or b == yn:
# #             print(f"Found {yn} {c} {a if a != yn else b}")
# #             counts[-1] += 1
# #             if c == "AND":
# #                 if has_and:
# #                     print("AND")
# #                 has_and = True
# #             elif c == "XOR":
# #                 if has_xor:
# #                     print("XOR")
# #                 has_xor = True
# # print(Counter(counts))
# # for i in range(100):
# #     zn = f"z{i:02d}"
# #     if zn not in nodes:
# #         break
# #     print(node_inps[zn])
#

print("=========================")
for n in nx.topological_sort(graph):
    if n in node_inps:
        a, b, c = node_inps[n]
        print(f"{min(a, b)} {c} {max(a, b)} -> {n}")
#
#
# a = ["mvb", "z08", "z18", "wss", "bmn", "z23", "jss", "rds"]
# print(",".join(sorted(a)))


def get_sus(node_inps: dict[str, tuple[str, str, str]], nodes: set[str], num_bits: int):
    xors_vars = []
    and_vars = []
    c_vars = []
    cand_vars = []

    first_c = ""
    for node in nodes:
        if node in node_inps:
            a, b, c = node_inps[node]
            if c == "AND" and a in ["x00", "y00"] and b in ["x00", "y00"]:
                first_c = node
                break

    for i in range(1, num_bits):
        xn, yn, _ = get_xyz(i)
        for node in nodes:
            if node in node_inps:
                a, b, c = node_inps[node]
                if (a == xn and b == yn) or (b == xn and a == yn):
                    if c == "XOR":
                        xors_vars.append(node)
                    elif c == "AND":
                        and_vars.append(node)
    for node in nodes:
        if node in node_inps:
            a, b, c = node_inps[node]
            if c == "OR":
                if node == f"z{num_bits:02d}":
                    continue
                c_vars.append(node)
    for node in nodes:
        if node in node_inps:
            a, b, c = node_inps[node]
            if c == "AND" and a[0] not in "xy" and b[0] not in "xy":
                cand_vars.append(node)
    sus: set[str] = set()
    for i in xors_vars:
        if i[0] == "z":
            sus.add(i)
    for i in and_vars:
        if i[0] == "z":
            sus.add(i)
    for i in c_vars:
        if i[0] == "z":
            sus.add(i)
    for i in cand_vars:
        if i[0] == "z":
            sus.add(i)
    for i in xors_vars:
        has_and = False
        has_xor = False
        for node in nodes:
            if node in node_inps:
                a, b, c = node_inps[node]
                if a == i or b == i:
                    if c == "XOR":
                        if has_xor:
                            sus.add(i)
                        if node[0] != "z":
                            sus.add(node)
                        if a == i:
                            if b not in c_vars and b != first_c:
                                sus.add(b)
                        elif b == i:
                            if a not in c_vars and a != first_c:
                                sus.add(a)
                        has_xor = True
                    elif c == "AND":
                        if has_and:
                            sus.add(i)
                        has_and = True
                        if a == i:
                            if b not in c_vars and b != first_c:
                                sus.add(b)
                        elif b == i:
                            if a not in c_vars and a != first_c:
                                sus.add(a)
                        if node not in cand_vars:
                            sus.add(node)
                    else:
                        sus.add(i)
        if not has_and or not has_xor:
            sus.add(i)
    for i in and_vars:
        has_or = False
        for node in nodes:
            if node in node_inps:
                a, b, c = node_inps[node]
                if a == i or b == i:
                    if c == "OR":
                        if has_or:
                            sus.add(i)
                        has_or = True
                        if a == i:
                            if b not in cand_vars:
                                sus.add(b)
                        elif b == i:
                            if a not in cand_vars:
                                sus.add(a)
                        if node not in c_vars and node != f"z{num_bits:02d}":
                            sus.add(node)
                    else:
                        sus.add(i)
        if not has_or:
            sus.add(i)
    for i in c_vars:
        has_and = False
        has_xor = False
        for node in nodes:
            if node in node_inps:
                a, b, c = node_inps[node]
                if a == i or b == i:
                    if c == "XOR":
                        if has_xor:
                            sus.add(i)
                        has_xor = True
                        if node[0] != "z":
                            sus.add(node)
                        if a == i:
                            if b not in xors_vars:
                                sus.add(b)
                        elif b == i:
                            if a not in xors_vars:
                                sus.add(a)
                    elif c == "AND":
                        if has_and:
                            sus.add(i)
                        has_and = True
                        if a == i:
                            if b not in xors_vars:
                                sus.add(b)
                        elif b == i:
                            if a not in xors_vars:
                                sus.add(a)
                        if node not in cand_vars:
                            sus.add(node)
                    else:
                        sus.add(i)
        if not has_and or not has_xor:
            sus.add(i)
    for i in cand_vars:
        has_or = False
        for node in nodes:
            if node in node_inps:
                a, b, c = node_inps[node]
                if a == i or b == i:
                    if c == "OR":
                        if has_or:
                            sus.add(i)
                        has_or = True
                        if a == i:
                            if b not in and_vars:
                                sus.add(b)
                        elif b == i:
                            if a not in and_vars:
                                sus.add(a)
                        if node not in c_vars and node != f"z{num_bits:02d}":
                            sus.add(node)
                    else:
                        sus.add(i)
        if not has_or:
            sus.add(i)
    return sus


sus = get_sus(node_inps, nodes, num_bits)


print(sus)
visited = set()
swaps = []
print(",".join(sorted(sus)))
