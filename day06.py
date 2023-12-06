from math import ceil, floor, sqrt

from common import get_input


def get_num_sols(time, dist):
    quad_inner = sqrt(time ** 2 - 4 * dist)
    l = ceil((-time - quad_inner) / 2)
    r = floor((-time + quad_inner) / 2)
    return r - l + 1


def part1():
    data = get_input(6)
    times = data[0].split(":")[1].split()
    distances = data[1].split(":")[1].split()

    product = 1
    for time, dist in zip(
        map(int, times),
        map(int, distances),
    ):
        product *= get_num_sols(time, dist)
    print(product)


def part2():
    data = get_input(6)
    times = data[0].split(":")[1].split()
    distances = data[1].split(":")[1].split()

    print(get_num_sols(
        int("".join(times)),
        int("".join(distances))
    ))


if __name__ == "__main__":
    part1()
    part2()
