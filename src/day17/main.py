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


rega = int(lines[0].split(" ")[-1])
regb = int(lines[1].split(" ")[-1])
regc = int(lines[2].split(" ")[-1])

prog = list(map(int, lines[-1].split(" ")[-1].split(",")))

print(rega, regb, regc, prog)


def combo_op(operand: int) -> int:
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return rega
    elif operand == 5:
        return regb
    elif operand == 6:
        return regc
    else:
        raise ValueError(f"Invalid operand {operand}")


# op_names = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']
# pc = 0
# result = []
# while pc < len(prog):
#     op = prog[pc]
#     operand = prog[pc + 1]
#     pc += 2
#     print(op_names[op], operand)
#     if op == 0:
#         rega = rega // (2 ** combo_op(operand))
#     elif op == 1:
#         regb = regb ^ operand
#     elif op == 2:
#         regb = combo_op(operand) & 0x7
#     elif op == 3:
#         if rega != 0:
#             pc = operand
#     elif op == 4:
#         regb = regb ^ regc
#     elif op == 5:
#         result.append(combo_op(operand) % 8)
#     elif op == 6:
#         regb = rega // (2 ** combo_op(operand))
#     elif op == 7:
#         regc = rega // (2 ** combo_op(operand))
#     else:
#         raise ValueError(f"Invalid op {op}")


def process(a: int) -> int:
    b = a & 7
    c = a >> (b ^ 7)
    return (b ^ c) & 7


def get_solution(a_val: int, prog_idx: int) -> list[int]:
    print(f"processing {a_val} {prog_idx} {prog[prog_idx]}")
    if prog_idx < 0:
        return [a_val]

    results = []
    new_a_val = a_val << 3
    for i in range(8):
        new_new_a_val = new_a_val + i
        if process(new_new_a_val) == prog[prog_idx]:
            res = get_solution(new_new_a_val, prog_idx - 1)
            results.extend(res)
    return results


rega = min(get_solution(7, len(prog) - 2))
sol = rega
op_names = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
pc = 0
result = []
while pc < len(prog):
    op = prog[pc]
    operand = prog[pc + 1]
    pc += 2
    print(op_names[op], operand)
    if op == 0:
        rega = rega // (2 ** combo_op(operand))
    elif op == 1:
        regb = regb ^ operand
    elif op == 2:
        regb = combo_op(operand) & 0x7
    elif op == 3:
        if rega != 0:
            pc = operand
    elif op == 4:
        regb = regb ^ regc
    elif op == 5:
        result.append(combo_op(operand) % 8)
    elif op == 6:
        regb = rega // (2 ** combo_op(operand))
    elif op == 7:
        regc = rega // (2 ** combo_op(operand))
    else:
        raise ValueError(f"Invalid op {op}")
print(",".join(map(str, result)))
print(",".join(map(str, prog)))
print(sol)
#
# print(result)
# print(','.join(map(str, result)))
