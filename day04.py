from common import get_input


def lines_to_win(data):
    data = get_input(4)
    ret = {}
    for i, line in enumerate(data):
        nums = line.split(": ")[1]
        winning, mine = nums.split(" | ")
        win_nums = set(map(int, winning.split()))
        mine_nums = set(map(int, mine.split()))
        winners = win_nums & mine_nums
        ret[i] = len(winners)
    return ret


def part1():
    data = get_input(4)
    l2w = lines_to_win(data)
    total = sum([2 ** (lwin - 1) if lwin else 0 for lwin in l2w.values()])
    print(total)


def part2():
    data = get_input(4)
    cards = len(data)
    l2w = lines_to_win(data)
    totals = {k: 1 for k in range(cards)}
    for i in range(cards-1):
        wins = l2w[i]
        start = i + 1
        end = min(cards, i+1+wins)
        num_is = totals[i]
        for j in range(start, end):
            totals[j] += num_is
    print(sum(totals.values()))


if __name__ == "__main__":
    part1()
    part2()
