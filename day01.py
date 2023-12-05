from common import get_input


def part1():
    data = get_input(1)
    total = 0
    for line in data:
        li = 0
        ri = len(line) - 1
        while not line[li].isdigit():
            li += 1
        left = int(line[li])
        while not line[ri].isdigit():
            ri -= 1
        right = int(line[ri])
        total += left*10+right
    print(total)


def part2():
    data = get_input(1)
    total = 0
    len3nums = {
        "one": 1,
        "two": 2,
        "six": 6,
    }
    len4nums = {
        "four": 4,
        "five": 5,
        "nine": 9,
    }
    len5nums = {
        "three": 3,
        "seven": 7,
        "eight": 8,
    }

    def str_num(cur):
        for dist, arr in (
            (3, len3nums),
            (4, len4nums),
            (5, len5nums),
        ):
            subs = line[cur:cur + dist]
            if subs in arr:
                return arr[subs]
        return None

    for line in data:
        li = 0
        ri = len(line) - 1
        left = None
        right = None
        while li < len(line):
            if line[li].isdigit():
                left = int(line[li])
                break
            left = str_num(li)
            if left is not None:
                break
            li += 1

        while ri > -1:
            if line[ri].isdigit():
                right = int(line[ri])
                break
            right = str_num(ri)
            if right is not None:
                break
            ri -= 1

        total += left*10+right
    print(total)


if __name__ == "__main__":
    part1()
    part2()
