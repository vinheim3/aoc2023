from common import get_input, make_md_array
from grid import Grid, get_surrounding


def fill_grid(center, grid, rounds):
    q = {(center, center)}
    for i in range(rounds):
        q = {
            (nx, ny) for x, y in q for nx, ny in get_surrounding(x, y)
            if 0 <= nx < grid.width and 0 <= ny < grid.height and grid.cell(nx, ny) == '.'
        }
    return q


def part1():
    grid = Grid(get_input(21))
    x, y = grid.find_ch('S')
    assert x == y and x == grid.width // 2  # S in the center is importannt for p2
    print("Part 1:", len(fill_grid(x, grid, 64)) + 1)  # include center due to even steps


def part2():
    grid = Grid(get_input(21))
    width, height = grid.width, grid.height
    cells_high = 26_501_365-width//2  # excluding the central grid
    assert cells_high % width == 0  # we can fill up to the top of the highest grid
    grids_high = cells_high // width
    assert grids_high % 2 == 0  # we can get the relevant values using a 5x5 grid (2 grids high)

    # Make new 5x5 grid of grids
    x, y = grid.find_ch('S')
    grid.grid[y][x] = '.'
    grid = Grid(make_md_array(width * 5, height * 5, lambda c, r: grid.cell(c % width, r % height)))

    # Fill grid
    center = width*2+width//2
    q = fill_grid(center, grid, center)

    grid_dims = []
    for _ in range(5):
        grid_dims.append([0]*5)

    for y in range(5):
        for x in range(5):
            xoffs, yoffs = x * width, y * width
            grid_dims[y][x] = sum(
                len([col for col in range(width) if (xoffs + col, yoffs + row) in q])
                for row in range(width)
            )

    total_even_layers = 1 + sum(i*4 for i in range(2, grids_high, 2))
    total_odd_layers = sum(i*4 for i in range(1, grids_high, 2))
    total_small_corners = grids_high
    total_big_unfilled_corners = grids_high - 1
    print(
        "Part 2:",
        total_even_layers * grid_dims[2][2] +
        total_odd_layers * grid_dims[1][2] +
        total_small_corners * (grid_dims[0][1] + grid_dims[0][3] + grid_dims[4][1] + grid_dims[4][3]) +
        total_big_unfilled_corners * (grid_dims[1][1] + grid_dims[1][3] + grid_dims[3][1] + grid_dims[3][3]) +
        grid_dims[0][2] + grid_dims[2][0] + grid_dims[2][4] + grid_dims[4][2]
    )


if __name__ == "__main__":
    part1()
    part2()
