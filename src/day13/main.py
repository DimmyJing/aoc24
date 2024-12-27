import copy
import math
import re
import sys
from functools import lru_cache

import networkx as nx
from pulp import *
from sympy import Matrix, simplify, solve_linear_system, symbols
from sympy.solvers.diophantine import diophantine
from sympy.solvers.simplex import lpmax

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


total = 0


# for i in range(math.ceil(len(lines) / 4)):
#     a = lines[i * 4]
#     b = lines[i * 4 + 1]
#     c = lines[i * 4 + 2]
#     aa = a.split("+")
#     ax = int(aa[1].split(",")[0])
#     ay = int(aa[2])
#     bb = b.split("+")
#     bx = int(bb[1].split(",")[0])
#     by = int(bb[2])
#     cc = c.split("=")
#     cx = int(cc[1].split(",")[0])
#     cy = int(cc[2])
#
#     maxp = max(
#         math.ceil(cx / ax), math.ceil(cy / ay), math.ceil(cx / bx), math.ceil(cy / by)
#     )
#     minres = float("inf")
#     for i in range(maxp + 4):
#         for j in range(maxp + 4):
#             if i * ax + j * bx == cx and i * ay + j * by == cy:
#                 res = i * 3 + j
#                 minres = min(minres, res)
#                 # print(i, j)
#                 # break
#     if minres != float("inf"):
#         total += minres
#     print(minres)


for idx in range(math.ceil(len(lines) / 4)):
    a = lines[idx * 4]
    b = lines[idx * 4 + 1]
    c = lines[idx * 4 + 2]
    aa = a.split("+")
    ax = int(aa[1].split(",")[0])
    ay = int(aa[2])
    bb = b.split("+")
    bx = int(bb[1].split(",")[0])
    by = int(bb[2])
    cc = c.split("=")
    cx = int(cc[1].split(",")[0])
    cy = int(cc[2])
    cx += 10000000000000
    cy += 10000000000000

    # maxa = max(math.ceil(cx / ax), math.ceil(cy / ay))
    # maxb = max(math.ceil(cx / bx), math.ceil(cy / by))
    #
    # a = LpVariable("a", lowBound=0, upBound=maxa, cat=LpInteger)
    # b = LpVariable("b", lowBound=0, upBound=maxb, cat=LpInteger)
    # prob = LpProblem("myProblem", LpMinimize)
    # prob += a * ax + b * bx == cx
    # prob += a * ay + b * by == cy
    # prob += a * 3 + b
    # status = prob.solve()
    # print(status)
    # aval: int = value(a)
    # bval: int = value(b)
    # if aval != round(aval) or bval != round(bval):
    #     continue
    # if aval * ax + bval * ay == cx and aval * bx + bval * by == cy:
    #     total += aval * 3 + bval
    # results.append((aval, bval))
    #
    # # # ax1 + by1 = z1
    # # # ax2 + by2 = z2
    # # maxp = max(
    # #     math.ceil(cx / ax), math.ceil(cy / ay), math.ceil(cx / bx), math.ceil(cy / by)
    # # )
    # # print(maxp)
    # # # minres = float("inf")
    # # # for i in range(maxp + 4):
    # # #     for j in range(maxp + 4):
    # # #         if i * ax + j * bx == cx and i * ay + j * by == cy:
    # # #             res = i * 3 + j
    # # #             minres = min(minres, res)
    # # #             # print(i, j)
    # # #             # break
    # # # if minres != float("inf"):
    # # #     total += minres
    # # # print(minres)
    gcd = math.gcd(ax, bx, cx)
    ax //= gcd
    bx //= gcd
    cx //= gcd
    gcd = math.gcd(ay, by, cy)
    ay //= gcd
    by //= gcd
    cy //= gcd
    a, b = symbols("a, b", integer=True)
    sola = diophantine(a * ax + b * bx - cx)
    a, b = symbols("a, b", integer=True)
    solb = diophantine(a * ay + b * by - cy)
    if len(sola) == 0:
        continue
    if len(solb) == 0:
        continue
    sola = next(iter(sola))
    solb = next(iter(solb))
    print(sola, solb)
    atxcoeff = 0
    acxcoeff = 0
    btxcoeff = 0
    bcxcoeff = 0
    atycoeff = 0
    acycoeff = 0
    btycoeff = 0
    bcycoeff = 0
    for i in sola[0].as_coefficients_dict():
        if i == 1:
            acxcoeff = int(sola[0].as_coefficients_dict()[i])
            bcxcoeff = int(sola[1].as_coefficients_dict()[i])
            acycoeff = int(solb[0].as_coefficients_dict()[i])
            bcycoeff = int(solb[1].as_coefficients_dict()[i])
        else:
            atxcoeff = int(sola[0].as_coefficients_dict()[i])
            btxcoeff = int(sola[1].as_coefficients_dict()[i])
            atycoeff = int(solb[0].as_coefficients_dict()[i])
            btycoeff = int(solb[1].as_coefficients_dict()[i])
    # if bcxcoeff < 0:
    #     t = -(bcxcoeff / btxcoeff)
    #     if t < 0:
    #         t = math.floor(t)
    #     else:
    #         t = math.ceil(t)
    #     bcxcoeff += t * btxcoeff
    #     acxcoeff += t * atxcoeff
    # if bcycoeff < 0:
    #     t = -(bcycoeff / btycoeff)
    #     if t < 0:
    #         t = math.floor(t)
    #     else:
    #         t = math.ceil(t)
    #     bcycoeff += t * btycoeff
    #     acycoeff += t * atycoeff
    # if acxcoeff < 0:
    #     t = -(acxcoeff / atxcoeff)
    #     if t < 0:
    #         t = math.floor(t)
    #     else:
    #         t = math.ceil(t)
    #     acxcoeff += t * atxcoeff
    #     bcxcoeff += t * btxcoeff
    # if acycoeff < 0:
    #     t = -(acycoeff / atycoeff)
    #     if t < 0:
    #         t = math.floor(t)
    #     else:
    #         t = math.ceil(t)
    #     acycoeff += t * atycoeff
    #     bcycoeff += t * btycoeff
    print(
        f"acxcoeff: {acxcoeff}, atxcoeff: {atxcoeff}, bcxcoeff: {bcxcoeff}, btxcoeff: {btxcoeff}"
    )
    print(
        f"acycoeff: {acycoeff}, atycoeff: {atycoeff}, bcycoeff: {bcycoeff}, btycoeff: {btycoeff}"
    )
    print(acxcoeff * ax + bcxcoeff * bx, acxcoeff * ay + bcxcoeff * by, cx, cy)
    # # print(
    # #     accoeff * ax + bccoeff * bx,
    # #     accoeff * ay + bccoeff * by,
    # #     cx / accoeff * ax + bccoeff * bx,
    # #     cy / accoeff * ay + bccoeff * by,
    # # )
    # binb = bin_search(atcoeff, accoeff, ay, btcoeff, bccoeff, by, cy)
    # print("solution", bina)

    tx, ty = symbols("tx, ty", integer=True)
    # res = lpmax(
    #     btxcoeff * tx + bcxcoeff,
    #     [
    #         atxcoeff * tx + acxcoeff == atycoeff * ty + acycoeff,
    #         btxcoeff * tx + bcxcoeff == btycoeff * ty + bcycoeff,
    #         atxcoeff * tx + acxcoeff >= 0,
    #         btxcoeff * tx + bcxcoeff >= 0,
    #     ]
    # )
    system = Matrix(
        (
            (atxcoeff, atycoeff, acycoeff - acxcoeff),
            (btxcoeff, btycoeff, bcycoeff - bcxcoeff),
        )
    )
    sol = solve_linear_system(system, tx, ty)
    txv = sol[tx]
    tyv = sol[ty]
    print(
        "alwijdalwijdalwidjailwjd",
        simplify(txv * atxcoeff + acxcoeff),
        simplify(tyv * atycoeff + acycoeff),
    )
    # tx = LpVariable("tx", cat=LpInteger)
    # ty = LpVariable("ty", cat=LpInteger)
    # prob = LpProblem("myProblem", LpMinimize)
    # prob += atxcoeff * tx + acxcoeff >= 0
    # prob += btxcoeff * tx + bcxcoeff >= 0
    # # prob += atycoeff * ty + acycoeff >= 0
    # # prob += btycoeff * ty + bcycoeff >= 0
    # prob += atxcoeff * tx + acxcoeff == atycoeff * ty + acycoeff
    # prob += btxcoeff * tx + bcxcoeff == btycoeff * ty + bcycoeff
    # prob += atxcoeff * tx + acxcoeff
    # status = prob.solve()
    # txval = int(value(tx))
    # av = txval * atxcoeff + acxcoeff
    # bv = txval * btxcoeff + bcxcoeff
    # print("a", av, "b", bv)
    # print(status)
    # if status == 1:
    #     total += av * 3 + bv
    # b = LpVariable("b", lowBound=0, upBound=maxb, cat=LpInteger)
    # prob += a * ax + b * bx == cx
    # prob += a * ay + b * by == cy
    # prob += a * 3 + b
    # status = prob.solve()
    # print(status)
    # aval: int = value(a)
    # bval: int = value(b)
    # if aval != round(aval) or bval != round(bval):
    #     continue
    # if aval * ax + bval * ay == cx and aval * bx + bval * by == cy:
    #     total += aval * 3 + bval
    # results.append((aval, bval))
print(total)


# axt(tx) + axc = ayt(ty) + ayc
# bxt(tx) + bxc = byt(ty) + byc

# axt(tx) - ayt(ty) = ayc - axc
# bxt(tx) - byt(ty) = byc - bxc

# [ axt, ayt ] [ tx ] = [ ayc - axc ]
# [ bxt, byt ] [ ty ] = [ byc - bxc ]
