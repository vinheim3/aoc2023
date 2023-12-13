from common import get_input, get_groups
from grid import Grid


def get_num_diff(dim1, dim2):
    pos1 = {i for i, ch in enumerate(dim1) if ch == '#'}
    pos2 = {i for i, ch in enumerate(dim2) if ch == '#'}
    same = pos1 & pos2
    return max(len(pos2-same), len(pos1-same))


def get_vert_equal(grid: Grid, lcol: int, diff1_allowed: bool) -> bool:
    li, ri = lcol, lcol+1
    while li >= 0 and ri < grid.width:
        diffs = get_num_diff(grid.get_col(li), grid.get_col(ri))
        if diffs > 1:
            return False
        elif diffs == 1:
            if diff1_allowed:
                diff1_allowed = False
            else:
                return False
        li -= 1
        ri += 1
    return True


def get_horiz_equal(grid: Grid, lrow: int, diff1_allowed: bool) -> bool:
    li, ri = lrow, lrow+1
    while li >= 0 and ri < grid.height:
        diffs = get_num_diff(grid.get_row(li), grid.get_row(ri))
        if diffs > 1:
            return False
        elif diffs == 1:
            if diff1_allowed:
                diff1_allowed = False
            else:
                return False
        li -= 1
        ri += 1
    return True


if __name__ == "__main__":
    data = get_groups(get_input(13))
    total = 0
    mapping = {}

    for pi, puzzle in enumerate(data):
        grid = Grid(puzzle)

        # try horiz
        horiz = None
        for i in range(grid.height - 1):
            if get_horiz_equal(grid, i, False):
                horiz = i + 1
                total += 100 * horiz
                mapping[pi] = ('h', horiz)
                break
        if horiz:
            continue

        # try vert
        vert = None
        if horiz is None:
            for i in range(grid.width - 1):
                if get_vert_equal(grid, i, False):
                    vert = i + 1
                    total += vert
                    mapping[pi] = ('v', vert)
                    break
        assert vert
    print("Part 1:", total)

    total = 0
    for pi, puzzle in enumerate(data):
        grid = Grid(puzzle)

        # try horiz
        horiz = None
        prev_valid = mapping[pi]
        for i in range(grid.height - 1):
            if prev_valid == ('h', i + 1):
                continue
            if get_horiz_equal(grid, i, True):
                horiz = i + 1
                total += 100 * horiz
                break
        if horiz:
            continue

        # try vert
        vert = None
        if horiz is None:
            for i in range(grid.width - 1):
                if prev_valid == ('v', i + 1):
                    continue
                if get_vert_equal(grid, i, True):
                    vert = i + 1
                    total += vert
                    break
        assert vert
    print("Part 2:", total)
