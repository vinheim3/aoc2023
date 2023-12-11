from itertools import combinations

from common import get_input


if __name__ == "__main__":
    data = [[*row] for row in get_input(11)]
    empty_rows = {i for (i, entry) in enumerate(data) if set(entry) == {'.'}}
    empty_cols = set(i for i in range(len(data[0])) if set(row[i] for row in data) == {'.'})
    galaxies = [(x, y) for y, row in enumerate(data) for x, col in enumerate(row) if col == '#']
    for expand in (2, 1_000_000):
        total = 0
        for pos1, pos2 in combinations(galaxies, 2):
            x1, y1 = pos1
            x2, y2 = pos2
            xs = set(range(x1, x2, 1 if x2 > x1 else -1))
            ys = set(range(y1, y2, 1 if y2 > y1 else -1))
            total += expand * (len(xs & empty_cols) + len(ys & empty_rows)) + len(xs - empty_cols) + len(ys - empty_rows)
        print(total)
