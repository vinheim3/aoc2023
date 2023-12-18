from collections import defaultdict

from common import get_input


def run(part1):
    entries = get_input(18)
    dirmap = {'R': 0, 'D': 1, 'L': 2, 'U': 3}

    x = y = minx = miny = maxx = maxy = 0
    row_entities = defaultdict(dict)  # turns and vertical pipes
    prev_dir = dirmap[entries[-1][0]] if part1 else int(entries[-1][-2])
    total = 0
    for entry in entries:
        dir_, val, col = entry.split()
        col = col[2:-1]

        val = int(val) if part1 else int(col[:5], 16)
        total += val

        dir_ = dirmap[dir_] if part1 else int(col[5])  # R D L U

        match dir_:
            case 0:  # R
                if prev_dir == 3:
                    row_entities[y][x] = '/'
                if prev_dir == 1:
                    row_entities[y][x] = '\\'
                x += val
                maxx = max(maxx, x)
            case 1:  # D
                if prev_dir == 0:
                    row_entities[y][x] = '\\'
                if prev_dir == 2:
                    row_entities[y][x] = '/'
                for i in range(y+1, y+val):
                    row_entities[i][x] = '|'
                y += val
                maxy = max(maxy, y)
            case 2:  # L
                if prev_dir == 3:
                    row_entities[y][x] = '\\'
                if prev_dir == 1:
                    row_entities[y][x] = '/'
                x -= val
                minx = min(minx, x)
            case 3:  # U
                if prev_dir == 0:
                    row_entities[y][x] = '/'
                if prev_dir == 2:
                    row_entities[y][x] = '\\'
                for i in range(y-1, y-val, -1):
                    row_entities[i][x] = '|'
                y -= val
                miny = min(miny, y)
        prev_dir = dir_

    for row in range(miny, maxy+1):
        ents = row_entities[row]
        out = True
        inwall = False
        closes_down = None
        ent_xs = list(sorted(ents.keys()))
        for i, ent_x in enumerate(ent_xs[:-1]):
            val = ents[ent_x]
            nextx = ent_xs[i+1]
            match val:
                case "|":
                    out = not out
                    if not out:
                        total += (nextx-1) - ent_x
                case "/":
                    if not inwall:
                        closes_down = True
                        inwall = True
                    else:
                        inwall = False
                        if closes_down:
                            out = not out
                        if not out:
                            total += (nextx - 1) - ent_x
                case "\\":
                    if not inwall:
                        closes_down = False
                        inwall = True
                    else:
                        inwall = False
                        if not closes_down:
                            out = not out
                        if not out:
                            total += (nextx - 1) - ent_x
    return total


if __name__ == "__main__":
    print("Part 1:", run(True))
    print("Part 2:", run(False))
