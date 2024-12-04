import sys

lines_raw = sys.stdin.readlines()
lines = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, lines_raw))
if lines[-1] == "":
    lines = lines[:-1]
lines_iter = iter(lines)


def good(level: list[int]):
    all_increasing = True
    temp = float("-inf")
    for i in level:
        if temp == float("-inf"):
            temp = i
            continue
        if i > temp:
            if i - temp >= 1 and i - temp <= 3:
                temp = i
            else:
                all_increasing = False
                break
        else:
            all_increasing = False
            break
    all_decreasing = True
    temp = float("inf")
    for i in level:
        if temp == float("inf"):
            temp = i
            continue
        if i < temp:
            if temp - i >= 1 and temp - i <= 3:
                temp = i
            else:
                all_decreasing = False
                break
        else:
            all_decreasing = False
            break
    return all_increasing or all_decreasing


total = 0
for line in lines:
    nums = list(map(int, line.split()))
    all_good = False
    for i in range(len(nums)):
        print(nums[:i] + nums[i + 1 :])
        if good(nums[:i] + nums[i + 1 :]):
            total += 1
            all_good = True
            break
    print(all_good)
print(total)
