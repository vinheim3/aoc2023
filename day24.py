from itertools import combinations
from z3 import Solver, Real, Reals, sat

from common import get_input


entries = get_input(24)
stones = []
equations = []
equation_map = {}
for entry in entries:
    l, r = entry.split('@')
    l = l.strip()
    r = r.strip()
    l = list(map(int, l.split(', ')))
    r = list(map(int, r.split(', ')))
    px, py, pz = l
    vx, vy, vz = r
    stones.append((px, py, pz, vx, vy, vz))

    slope = vy / vx
    c = px * slope - py
    equations.append((slope, c))
    equation_map[(slope, c)] = (px, py, vx, vy)


def part1():
    total = 0
    for (slope1, c1), (slope2, c2) in combinations(equations, 2):
        if slope1 == slope2:
            continue
        intersectx = (c1 - c2) / (slope1-slope2)
        intersecty = ((c1 * slope2) - (c2 * slope1)) / (slope1-slope2)

        def in_past(intersectx, px, vx, intersecty, py, vy):
            return (
                (vx < 0 and intersectx > px) or
                (vx > 0 and intersectx < px) or
                (vy < 0 and intersecty > py) or
                (vy > 0 and intersecty < py)
            )

        px, py, vx, vy = equation_map[(slope1, c1)]
        if in_past(intersectx, px, vx, intersecty, py, vy):
            continue
        px, py, vx, vy = equation_map[(slope2, c2)]
        if in_past(intersectx, px, vx, intersecty, py, vy):
            continue

        l, r = 200000000000000, 400000000000000
        if l <= intersectx <= r and l <= intersecty <= r:
            total += 1
    print("Part 1:", total)


def part2():
    pxr, pyr, pzr, vxr, vyr, vzr = Reals("pxr pyr pzr vxr vyr vzr")
    s = Solver()
    for i, (pxs, pys, pzs, vxs, vys, vzs) in enumerate(stones[:3]):
        time = Real(f"time_{i}")
        s.add(pxr + time * vxr == pxs + time * vxs)
        s.add(pyr + time * vyr == pys + time * vys)
        s.add(pzr + time * vzr == pzs + time * vzs)
    assert s.check() == sat
    model = s.model()
    print("Part 2:", sum(model[k].as_long() for k in (pxr, pyr, pzr)))


if __name__ == "__main__":
    part1()
    part2()
