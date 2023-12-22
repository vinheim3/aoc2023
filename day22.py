from copy import deepcopy
from collections import defaultdict

from common import get_input


if __name__ == "__main__":
    entries = get_input(22)
    z_bricks = []  # list of dicts for each z: map xy tuple to a brick id
    brick_dims = {}
    for i, entry in enumerate(entries):
        l, r = entry.split('~')
        x1, y1, z1 = list(map(int, l.split(',')))
        x2, y2, z2 = list(map(int, r.split(',')))
        assert z1 <= z2
        brick_dims[i] = (x1, y1, z1, x2, y2, z2)
        for z in range(z1, z2+1):
            if z+1 >= len(z_bricks):
                for _ in range(len(z_bricks), z+2):
                    z_bricks.append({})
            for y in range(y1, y2+1):
                for x in range(x1, x2+1):
                    z_bricks[z][(x, y)] = i

    def drop_all_bricks(z_bricks, brick_dims):
        fell = set()
        bricks_in_air = True
        while bricks_in_air:
            bricks_in_air = False
            for i, (x1, y1, z1, x2, y2, z2) in brick_dims.items():
                if z1 == 1:
                    continue
                if not any((x, y) in z_bricks[z1-1] for y in range(y1, y2+1) for x in range(x1, x2+1)):
                    bricks_in_air = True
                    fell.add(i)
                    brick_dims[i] = (x1, y1, z1 - 1, x2, y2, z2 - 1)
                    for y in range(y1, y2 + 1):
                        for x in range(x1, x2 + 1):
                            del z_bricks[z2][(x, y)]
                            z_bricks[z1 - 1][(x, y)] = i
        return fell

    drop_all_bricks(z_bricks, brick_dims)

    brick_supports = {}  # map bricks to the brick ids they support above
    support_cnts = defaultdict(int)  # map bricks to how many bricks support them below
    for i, (x1, y1, z1, x2, y2, z2) in brick_dims.items():
        aboves = {z_bricks[z2+1].get((x, y), -1) for y in range(y1, y2+1) for x in range(x1, x2+1)} - {-1}
        brick_supports[i] = aboves
        for val in aboves:
            support_cnts[val] += 1

    one_supporter = {k for k, v in support_cnts.items() if v == 1}  # only 1 brick supports me below
    # get bricks that are not the sole ones supporting a brick above
    can_remove = {i for i, support in brick_supports.items() if not (support & one_supporter)}
    print("Part 1:", len(can_remove))

    total = 0
    for i, (x1, y1, z1, x2, y2, z2) in brick_dims.items():
        new_z_bricks = deepcopy(z_bricks)
        new_brick_dims = deepcopy(brick_dims)
        for z in range(z1, z2 + 1):
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    del new_z_bricks[z][(x, y)]
        del new_brick_dims[i]

        total += len(drop_all_bricks(new_z_bricks, new_brick_dims))

    print("Part 2:", total)
