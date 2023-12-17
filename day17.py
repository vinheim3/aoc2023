from common import get_input
from grid import Grid, Dirs, get_surrounding_with_dirs


def run(ultra):
    grid = Grid(get_input(17))

    x, y = grid.width - 1, grid.height - 1
    heat_loss = int(grid.cell(x, y))
    min_heat = {
        (x - 1, y, Dirs.W, 1): heat_loss + int(grid.cell(x-1, y)),
        (x, y - 1, Dirs.N, 1): heat_loss + int(grid.cell(x, y-1))
    }
    # x, y, dir of new, num straight lines so far, heat loss
    to_calc = {
        (x-1, y, Dirs.W, 1, min_heat[(x-1, y, Dirs.W, 1)]),
        (x, y-1, Dirs.N, 1, min_heat[(x, y-1, Dirs.N, 1)])
    }
    max_straight = 10 if ultra else 3

    while to_calc:
        x, y, dir_, num_dir_lines, heat_loss = to_calc.pop()
        for sx, sy, sdir in get_surrounding_with_dirs(x, y):
            if 0 <= sx < grid.width and 0 <= sy < grid.height:
                if dir_ == sdir:
                    if num_dir_lines == max_straight:
                        continue
                    new_num_dir_lines = num_dir_lines + 1
                elif (dir_.value ^ sdir.value) & 1 == 1:  # turn only
                    if ultra and not (4 <= num_dir_lines <= 10):
                        continue
                    new_num_dir_lines = 1
                else:
                    continue

                key = (sx, sy, sdir, new_num_dir_lines)
                new_heat_loss = heat_loss + int(grid.cell(sx, sy))
                if new_heat_loss > min_heat.get(key, 1_000_000):
                    continue
                min_heat[key] = new_heat_loss
                to_calc.add((sx, sy, sdir, new_num_dir_lines, new_heat_loss))

    return min(v for k, v in min_heat.items() if k[0] == 0 and k[1] == 0) - int(grid.cell(0, 0))


if __name__ == "__main__":
    print("Part 1:", run(False))
    print("Part 2:", run(True))
