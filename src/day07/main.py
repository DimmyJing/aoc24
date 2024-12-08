import re
import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)


def solve_rec(num: int, nums: list[int], current: int) -> bool:
    if len(nums) == 0:
        return current == num
    start = nums[0]
    rest = nums[1:]
    if solve_rec(num, rest, current + start):
        return True
    if solve_rec(num, rest, current * start):
        return True
    if solve_rec(num, rest, int(str(current) + str(start))):
        return True
    return False


def solve(num: int, nums: list[int]) -> bool:
    return solve_rec(num, nums[1:], nums[0])


total = 0
for line in lines:
    nums = line.split()
    nums[0] = nums[0][:-1]
    nums = list(map(int, nums))
    start = nums[0]
    rest = nums[1:]
    print(start, rest)
    if solve(start, rest):
        total += start
        print("YES")
    else:
        print("NO")
print(total)
