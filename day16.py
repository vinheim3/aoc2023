from typing import List

from common import get_input, make_md_array
from grid import Grid, GridEntity, Dirs


def move_beam(grid: Grid, beam: GridEntity, visited: List[List[List[bool]]]) -> List[GridEntity]:
    if not beam.move(grid):
        return []

    dirv = beam.dir.value
    if visited[beam.y][beam.x][dirv] is True:
        return []
    visited[beam.y][beam.x][dirv] = True

    match grid.cell(beam.x, beam.y):
        case "/":
            beam.reflect_fw_slash()
        case "\\":
            beam.reflect_bw_slash()
        case "|":
            if beam.dir in (Dirs.E, Dirs.W):
                return beam.split_vert()
        case "-":
            if beam.dir in (Dirs.N, Dirs.S):
                return beam.split_horiz()

    return [beam]


def get_energy(grid: Grid, orig_beam: GridEntity):
    visited = make_md_array(grid.width, grid.height, lambda c, r: [False]*4)

    beams = [orig_beam]
    while beams:
        new_beams = []
        for beam in beams:
            new_beams.extend(move_beam(grid, beam, visited))
        beams = new_beams

    return sum(
        sum(map(lambda cell: 1 if True in cell else 0, row))
        for row in visited
    )


if __name__ == "__main__":
    grid = Grid(get_input(16))

    p1 = get_energy(grid, GridEntity(-1, 0, Dirs.E))
    print("Part 1:", p1)

    max_energy = p1
    for i in range(grid.height):
        if i != 0:
            max_energy = max(max_energy, get_energy(grid, GridEntity(-1, i, Dirs.E)))
        max_energy = max(max_energy, get_energy(grid, GridEntity(grid.width, i, Dirs.W)))
    for i in range(grid.width):
        max_energy = max(max_energy, get_energy(grid, GridEntity(i, -1, Dirs.S)))
        max_energy = max(max_energy, get_energy(grid, GridEntity(i, grid.height, Dirs.N)))
    print("Part 2:", max_energy)
