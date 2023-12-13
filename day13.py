from typing import Callable, List

from common import get_input, get_groups
from grid import Grid


def get_dim_equal(grid: Grid, is_cols: bool, dimi: int, diff1_allowed: bool) -> bool:
    li, ri = dimi, dimi+1
    end = grid.width if is_cols else grid.height
    while li >= 0 and ri < end:
        f: Callable[[int], List[str]] = grid.get_col if is_cols else grid.get_row
        pos1 = {i for i, ch in enumerate(f(li)) if ch == '#'}
        pos2 = {i for i, ch in enumerate(f(ri)) if ch == '#'}
        same = pos1 & pos2
        diffs = max(len(pos2 - same), len(pos1 - same))
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
            if get_dim_equal(grid, False, i, False):
                horiz = i + 1
                total += 100 * horiz
                mapping[pi] = ('h', i)
                break
        if horiz:
            continue

        # try vert
        vert = None
        if horiz is None:
            for i in range(grid.width - 1):
                if get_dim_equal(grid, True, i, False):
                    vert = i + 1
                    total += vert
                    mapping[pi] = ('v', i)
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
            if prev_valid == ('h', i):
                continue
            if get_dim_equal(grid, False, i, True):
                horiz = i + 1
                total += 100 * horiz
                break
        if horiz:
            continue

        # try vert
        vert = None
        if horiz is None:
            for i in range(grid.width - 1):
                if prev_valid == ('v', i):
                    continue
                if get_dim_equal(grid, True, i, True):
                    vert = i + 1
                    total += vert
                    break
        assert vert
    print("Part 2:", total)
