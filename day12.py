from functools import cache

from common import get_input


@cache
def trim_dots(arr: tuple):
    if not arr:
        return ()
    l, r = 0, len(arr) - 1
    while arr[l] == '.':
        l += 1
    while arr[r] == '.':
        r -= 1
    return arr[l:r+1]


@cache
def num_valid(springs, nums):
    # no more springs to process = 1 if all nums are processed
    if not springs:
        return 1 if not nums else 0

    # no more nums to process = 1 valid solution if a combo of . and ?
    if not nums:
        return 1 if '#' not in springs else 0

    springs = trim_dots(springs)
    total = 0

    num = nums[0]
    nums = nums[1:]
    ls = len(springs)

    for i, end in zip(range(ls-num+1), range(num, ls+1)):
        # if the sub-spring follows a #, we failed to match
        if '#' in springs[:i]:
            return total

        # if there is a . in the expected chars, match failed
        if '.' in springs[i:end]:
            continue

        # if there is an extra spring, return 0
        if end != ls and springs[end] == '#':
            continue

        total += num_valid(springs[end+1:], nums)
    return total


def part1_2():
    data = get_input(12)

    part1 = part2 = 0
    for i, entry in enumerate(data):
        springs, nums = entry.split()
        springs = tuple(ch for ch in springs)
        nums = tuple(map(int, nums.split(',')))

        part1 += num_valid(springs, nums)
        part2 += num_valid(springs + (("?",) + springs) * 4, nums*5)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    part1_2()
