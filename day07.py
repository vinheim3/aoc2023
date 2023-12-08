from collections import Counter

from common import get_input


def solution(joker):
    data = get_input(7)

    if joker:
        score_order = "AKQT98765432J"
    else:
        score_order = "AKQJT98765432"

    score_map = {letter: 12 - i for i, letter in enumerate(score_order)}
    fives, fours, full, threes, twos, ones, highs = [], [], [], [], [], [], []

    for line in data:
        l, r = line.split()
        bid = int(r)
        c = Counter(l)
        mc = c.most_common()

        if joker:
            if l == 'JJJJJ':
                fives.append((l, bid))
                continue

            mc = [item for item in mc if item[0] != 'J']

            if 'J' in l:
                mc1 = mc[0][1]
                mc = Counter(
                    l.replace('J', sorted(
                        [
                            item[0]
                            for item in mc
                            if item[1] == mc1 and item[0] != 'J'
                        ],
                        key=lambda item: score_map[item[0]],
                        reverse=True
                    )[0])
                ).most_common()

        mc1 = mc[0][1]
        if mc1 == 5:
            arr = fives
        else:
            mc2 = mc[1][1]
            if mc1 == 4:
                arr = fours
            elif mc1 == 3 and mc2 == 2:
                arr = full
            elif mc1 == 3:
                arr = threes
            elif mc1 == 2 and mc2 == 2:
                arr = twos
            elif mc1 == 2:
                arr = ones
            else:
                arr = highs

        arr.append((l, bid))

    new_items = []
    for arr in (fives, fours, full, threes, twos, ones, highs):
        new_items.extend(sorted(
            arr,
            key=lambda item: [
                score_map[letter]
                for i, letter in enumerate(item[0])
            ],
            reverse=True
        ))

    print(sum(
        item[1] * rank
        for item, rank in zip(new_items, range(len(new_items), 0, -1))
    ))


if __name__ == "__main__":
    solution(False)
    solution(True)
