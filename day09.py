from functools import reduce

from common import get_input


def get_histories(line):
    h = list(map(int, line.split()))
    hs = [h]
    while set(h) != {0}:
        h = [h[i+1] - h[i] for i in range(len(h)-1)]
        hs.append(h)
    return hs


def part1():
    data = get_input(9)
    print(sum(sum(row[-1] for row in get_histories(line)[-1::-1]) for line in data))


def part2():
    data = get_input(9)
    print(sum(reduce(lambda a, n: n[0] - a, get_histories(line)[-1::-1], 0) for line in data))


if __name__ == "__main__":
    part1()
    part2()
