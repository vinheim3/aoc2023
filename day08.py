from math import lcm

from common import get_input


data = get_input(8)
dirs = [1 if ch == "R" else 0 for ch in data[0]]
mapping = {}
for line in data[2:]:
    node, r = line.split(" = ")
    left, right = r.split(", ")
    mapping[node] = (left[1:], right[:-1])


def get_steps(curr, part_1):
    steps = 0
    while 1:
        for dir in dirs:
            steps += 1
            curr = mapping[curr][dir]

            if part_1:
                if curr == "ZZZ":
                    return steps
            else:
                if curr[2] == "Z":
                    return steps


def part1():
    print(get_steps("AAA", True))


def part2():
    print(lcm(*[get_steps(node, False) for node in mapping if node[2] == "A"]))


if __name__ == "__main__":
    part1()
    part2()
