from functools import cache

from common import get_input
from grid import Grid


def get_load(grid):
    height = grid.height
    return sum(
        sum([height - i for i, ch in enumerate(col) if ch == 'O'])
        for col in grid.get_cols()
    )


@cache
def move_up(col: tuple):
    new_regs = tuple()
    for reg in "".join(col+('#',)).split('#'):
        os = reg.count('O')
        new_regs += (('O',)*os + ('.',)*(len(reg)-os) + ('#',))
    return new_regs[:-2]  # exclude last group's # and extra terminating #


@cache
def move_down(col: tuple):
    return tuple(reversed(move_up(tuple(reversed(col)))))


if __name__ == "__main__":
    grid = Grid(get_input(14))
    move = 0  # N W S E
    seen = {}
    loopi = 0

    while 1:
        match move:
            case 0:
                for i, col in enumerate(grid.get_cols()):
                    grid.set_col(i, list(move_up(tuple(col))))
            case 1:
                for i, row in enumerate(grid.get_rows()):
                    grid.set_row(i, list(move_up(tuple(row))))
            case 2:
                for i, col in enumerate(grid.get_cols()):
                    grid.set_col(i, list(move_down(tuple(col))))
            case 3:
                for i, row in enumerate(grid.get_rows()):
                    grid.set_row(i, list(move_down(tuple(row))))

        curr = tuple(tuple(row) for row in grid.grid)
        if curr in seen:
            loop_count = loopi - seen[curr]
            first = seen[curr]
            bill_same_idx = ((4_000_000_000 - 1 - first) % loop_count) + first
            print("Part 1:", get_load(Grid([k for k, v in seen.items() if v == 0][0])))
            print("Part 2:", get_load(Grid([k for k, v in seen.items() if v == bill_same_idx][0])))
            break
        else:
            seen[curr] = loopi
        move = (move + 1) % 4
        loopi += 1
