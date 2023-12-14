from common import get_input
from grid import Grid


def get_load(grid):
    height = grid.height
    return sum(
        sum([height - i for i, ch in enumerate(grid.get_col(coli)) if ch == 'O'])
        for coli in range(grid.width)
    )


def move_up(col):
    new_col = []
    col.append('#')
    for reg in "".join(col).split('#'):
        os = reg.count('O')
        new_col.extend(['O'] * os)
        new_col.extend(['.'] * (len(reg) - os))
        new_col.append('#')
    return new_col[:-2]  # exclude last group's #, and extra terminating #


if __name__ == "__main__":
    grid = Grid(get_input(14))
    move = 0  # N W S E
    seen = {}
    loopi = 0

    while 1:
        match move:
            case 0:
                for i in range(grid.width):
                    new_col = move_up(grid.get_col(i))
                    for j in range(grid.height):
                        grid.grid[j][i] = new_col[j]
                if loopi == 0:
                    print("Part 1:", get_load(grid))
            case 1:
                for i in range(grid.height):
                    new_row = move_up(grid.get_row(i))
                    grid.grid[i] = new_row
            case 2:
                for i in range(grid.width):
                    new_col = list(reversed(move_up(list(reversed(grid.get_col(i))))))
                    for j in range(grid.height):
                        grid.grid[j][i] = new_col[j]
            case 3:
                for i in range(grid.height):
                    new_row = move_up(list(reversed(grid.get_row(i))))
                    grid.grid[i] = list(reversed(new_row))

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
