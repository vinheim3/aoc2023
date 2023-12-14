from functools import cache, reduce
from operator import add

from common import get_input
from grid import Grid


def get_load(grid):
    height = grid.height
    return sum(
        sum([height - i for i, ch in enumerate(grid.get_col(coli)) if ch == 'O'])
        for coli in range(grid.width)
    )


@cache
def move_up(col: tuple):
    new_regs = []
    for reg in "".join(col+('#',)).split('#'):
        os = reg.count('O')
        new_regs.append(('O',)*os + ('.',)*(len(reg)-os) + ('#',))
    return reduce(add, new_regs, ())[:-2]


if __name__ == "__main__":
    grid = Grid(get_input(14))
    move = 0  # N W S E
    seen = {}
    loopi = 0

    while 1:
        match move:
            case 0:
                for i in range(grid.width):
                    grid.set_col(i, move_up(tuple(grid.get_col(i))))
                if loopi == 0:
                    print("Part 1:", get_load(grid))
            case 1:
                for i in range(grid.height):
                    grid.grid[i] = list(move_up(tuple(grid.get_row(i))))
            case 2:
                for i in range(grid.width):
                    grid.set_col(i, list(reversed(move_up(tuple(reversed(grid.get_col(i)))))))
            case 3:
                for i in range(grid.height):
                    grid.grid[i] = list(reversed(move_up(tuple(reversed(grid.get_row(i))))))

        curr = tuple(tuple(row) for row in grid.grid)
        if curr in seen:
            loop_count = loopi - seen[curr]
            first = seen[curr]
            bill_same_idx = ((4_000_000_000 - 1 - first) % loop_count) + first
            print("Part 2:", get_load(Grid([k for k, v in seen.items() if v == bill_same_idx][0])))
            break
        else:
            seen[curr] = loopi
        move = (move + 1) % 4
        loopi += 1
