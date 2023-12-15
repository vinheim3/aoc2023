from common import get_input
from grid import Grid


grid = Grid(get_input(10))


def get_next(prev, todo):
    x, y = todo
    match grid.cell(x, y):
        case '7':
            return (x - 1, y) if prev[0] == x else (x, y + 1)
        case 'F':
            return (x + 1, y) if prev[0] == x else (x, y + 1)
        case 'L':
            return (x + 1, y) if prev[0] == x else (x, y - 1)
        case 'J':
            return (x - 1, y) if prev[0] == x else (x, y - 1)
        case '-':
            return (x + 1, y) if prev[0] < x else (x - 1, y)
        case '|':
            return (x, y + 1) if prev[1] < y else (x, y - 1)


if __name__ == "__main__":
    # Find initial position
    x, y = None, None
    for y, line in enumerate(grid.get_rows()):
        if 'S' in line:
            x = line.index('S')
            break
    assert x is not None and y is not None

    # Get initial cells to check
    prev1 = prev2 = (x, y)
    cells = []
    s_candidate = set("7FLJ-|")
    if grid.cell(x-1, y) in "FL-":
        cells.append((x - 1, y))
        s_candidate -= set("FL|")
    if grid.cell(x+1, y) in "7J-":
        cells.append((x + 1, y))
        s_candidate -= set("7J|")
    if grid.cell(x, y-1) in "F7|":
        cells.append((x, y - 1))
        s_candidate -= set("7F-")
    if grid.cell(x, y+1) in "LJ|":
        cells.append((x, y + 1))
        s_candidate -= set("JL-")
    cell1, cell2 = filter(None, cells)
    found = {prev1, prev2, cell1, cell2}
    grid.grid[y][x] = s_candidate.pop()

    # Follow path, exiting once the loop is re-found
    cntr = 0
    while 1:
        cntr += 1
        new_cell1 = get_next(prev1, cell1)
        new_cell2 = get_next(prev2, cell2)
        if new_cell1 in found or new_cell2 in found:
            found |= {new_cell1, new_cell2}
            break
        found |= {new_cell1, new_cell2}
        prev1, prev2, cell1, cell2 = cell1, cell2, new_cell1, new_cell2
    print("Part 1:", cntr)

    # Re-gen grid, but only with the loop tiles in
    only_loop = []
    width = grid.width
    for _ in range(grid.height):
        only_loop.append(['.'] * width)
    for x, y in found:
        only_loop[y][x] = grid.cell(x, y)

    # Expand horizontally
    new = []
    for line in only_loop:
        curr = []
        for ch in line:
            curr.append(ch)
            curr.append('-' if ch in 'LF-' else '.')
        new.append(curr)

    # Expand vertically
    new2 = []
    for line in new:
        curr = []
        curr2 = []
        for ch in line:
            curr.append(ch)
            curr2.append('|' if ch in '7F|' else '.')
        new2.append(curr)
        new2.append(curr2)

    # Get the tiles connected to the outside
    outside = []
    height, width = len(new2), len(new2[0])
    for i, ch in enumerate(new2[0]):
        if ch == '.':
            outside.append((i, 0))
    for i, ch in enumerate(new2[-1]):
        if ch == '.':
            outside.append((i, height-1))
    for i, row in enumerate(new2):
        if row[0] == '.':
            outside.append((0, i))
        if row[-1] == '.':
            outside.append((width-1, i))

    # Flood-fill
    while outside:
        x, y = outside.pop()
        if width > x >= 0 and height > y >= 0 and new2[y][x] == '.':
            new2[y][x] = 'O'
            outside.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

    # Count the untouched in-loop tiles from the original grid
    print("Part 2:", sum(line[::2].count(".") for line in new2[::2]))
