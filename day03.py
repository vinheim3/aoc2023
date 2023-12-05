from common import get_input


def part1():
    data = get_input(3)
    width = len(data[0])
    height = len(data)
    total = 0

    def has_adj_symbols(x, y, nlen):
        chars = []
        for ignore_lno, diff_y in (
            (0, -1),
            (height - 1, 1)
        ):
            if y != ignore_lno:
                oline = data[y+diff_y]
                for i in range(x-1, x+nlen+1):
                    if i < 0:
                        continue
                    if i >= width:
                        break
                    chars.append(oline[i])
        if x != 0:
            chars.append(data[y][x-1])
        if x+nlen != width:
            chars.append(data[y][x+nlen])
        return bool(set(chars)-set("0123456789."))

    for lno, line in enumerate(data):
        cur = 0
        while cur < width:
            if line[cur].isdigit():
                end = cur + 1
                while line[cur:end].isdigit() and end != width+1:
                    end += 1
                if end == width+1:
                    end += 1
                num = line[cur:end-1]
                num_len = len(num)
                if has_adj_symbols(cur, lno, num_len):
                    total += int(num)
                cur = end
            else:
                cur += 1

    print(total)


def part2():
    data = get_input(3)
    width = len(data[0])
    height = len(data)
    total = 0

    for lno, line in enumerate(data):
        cur = 0
        while cur < width:
            if line[cur] == '*':
                num_pos = []
                for ignore_lno, diff_y in (
                    (0, -1),
                    (height-1, 1)
                ):
                    if lno != ignore_lno:
                        oline = data[lno+diff_y][cur-1:cur+2]
                        if oline[1] == '.' and oline[0].isdigit() and oline[2].isdigit():
                            num_pos.append((lno+diff_y, cur - 1))
                            num_pos.append((lno+diff_y, cur + 1))
                        else:
                            for i, ch in enumerate(oline):
                                if ch.isdigit():
                                    num_pos.append((lno+diff_y, cur - 1 + i))
                                    break

                if cur != 0 and line[cur-1].isdigit():
                    num_pos.append((lno, cur - 1))

                if cur != width-1 and line[cur+1].isdigit():
                    num_pos.append((lno, cur + 1))

                if len(num_pos) == 2:
                    nums = []
                    for lineno, pos in num_pos:
                        nline = data[lineno]
                        l, r = pos, pos
                        while l >= 0 and nline[l].isdigit():
                            l -= 1
                        l += 1
                        while r <= width-1 and nline[r].isdigit():
                            r += 1
                        r -= 1
                        nums.append(nline[l:r+1])
                    total += int(nums[0])*int(nums[1])
            cur += 1
    print(total)


if __name__ == "__main__":
    part1()
    part2()
