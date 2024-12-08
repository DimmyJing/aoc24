import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)

adj_list = {}

doing_query = False
queries = []
for line in lines:
    if line == "":
        doing_query = True
        continue
    if not doing_query:
        a, b = map(int, line.split("|"))
        if a not in adj_list:
            adj_list[a] = []
        if b not in adj_list:
            adj_list[b] = []
        adj_list[a].append(b)
    else:
        nums = list(map(int, line.split(",")))
        queries.append(nums)


# def fix_ordering(query, adj_list):
#     incorrect_idx = None
#     for i, item in enumerate(query):
#         for child in adj_list[item]:
#             try:
#                 idx = query.index(child)
#             except ValueError:
#                 idx = -1
#             if idx != -1 and idx <= i:
#                 incorrect_idx = idx
#                 break
#     if incorrect_idx is None:
#         return query
#     incorrect_el = query[incorrect_idx]
#     smallest = incorrect_idx
#     for child in adj_list[incorrect_el]:
#         try:
#             idx = query.index(child)
#         except ValueError:
#             idx = -1
#         if idx != -1 and idx < incorrect_idx:
#             if smallest is None or query[idx] < query[smallest]:
#                 smallest = idx
#     query.pop(incorrect_idx)
#     query.insert(smallest, incorrect_el)
#     return fix_ordering(query, adj_list)


def top_sort(query: list[int], adj_list: dict[int, list[int]]):
    els = []
    for el in query:
        children = set()
        for child in adj_list[el]:
            if query.count(child) == 0:
                continue
            children.add(child)
        els.append((el, children))
    result = []
    while len(els) > 0:
        print(els)
        thing = None
        for idx, (el, children) in enumerate(els):
            if len(children) == 0:
                thing = els.pop(idx)
                break
        el, children = thing
        result.append(el)
        for idx, (el2, children) in enumerate(els):
            if el in children:
                children.remove(el)
                els[idx] = (el2, children)
    return result


total = 0
for query in queries:
    good = True
    for i, item in enumerate(query):
        for child in adj_list[item]:
            try:
                idx = query.index(child)
            except ValueError:
                idx = -1
            if idx != -1 and idx <= i:
                good = False
                break
    if good:
        # total += query[len(query) // 2]
        # print("good", query)
        pass
    else:
        print("before", query)
        query = top_sort(query, adj_list)
        # print(query[len(query) // 2])
        print("after", query)
        total += query[len(query) // 2]
# print(adj_list)
# print(queries)
print(total)
