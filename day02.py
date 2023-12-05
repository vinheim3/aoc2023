from collections import defaultdict

from common import get_input


def part1():
    data = get_input(2)
    total = 0
    maxs = {"red": 12, "green": 13, "blue": 14}
    for line in data:
        _game_id, _games = line.split(": ")
        game_id = int(_game_id.split()[1])

        games = _games.split("; ")
        possible = True
        for game in games:
            els = game.split(", ")
            for el in els:
                value, col = el.split()
                if int(value) > maxs[col]:
                    possible = False
                    break
            if not possible:
                break
        if possible:
            total += game_id
    print(total)


def part2():
    data = get_input(2)
    total = 0
    for line in data:
        _game_id, _games = line.split(": ")

        games = _games.split("; ")
        mins = defaultdict(int)
        for game in games:
            els = game.split(", ")
            for el in els:
                value, col = el.split()
                val = int(value)
                mins[col] = max(val, mins[col])
        power = mins["red"] * mins["green"] * mins["blue"]
        total += power
    print(total)


if __name__ == "__main__":
    part1()
    part2()
