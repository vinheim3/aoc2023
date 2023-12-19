from math import prod

from common import get_input, get_groups

g1, g2 = get_groups(get_input(19))
workflows = {}
for entry in g1:
    li = entry.index('{')
    workflows[entry[:li]] = entry[li+1:-1].split(",")


def part1():
    def get_accepted(steps, vals):
        step = steps[0]
        if step == 'A':
            return True
        if step == 'R':
            return False

        if ':' not in step:
            return get_accepted(workflows[step], vals)
        l, wf = step.split(':')
        var, cond, val = l[0], l[1], int(l[2:])
        assert cond in '<>'
        if (cond == '>' and vals[var] > val) or (cond == '<' and vals[var] < val):
            return get_accepted([wf] if wf in 'AR' else workflows[wf], vals)
        return get_accepted(steps[1:], vals)

    total = 0
    for entry in g2:
        vals = {k: 0 for k in 'xmas'}
        vars = entry[1:-1].split(",")
        for var in vars:
            lbl, val = var.split('=')
            vals[lbl] = int(val)

        if get_accepted(workflows['in'], vals):
            total += sum(vals.values())

    print("Part 1:", total)


def part2():
    def get_combos(val_ranges):
        return prod(end-start+1 for start, end in val_ranges.values())

    def get_step_combos(steps, val_ranges):
        step = steps[0]
        if step == 'A':
            return get_combos(val_ranges)
        if step == 'R':
            return 0

        if ':' not in step:
            return get_step_combos(workflows[step], val_ranges)
        l, wf = step.split(':')
        var, cond, val = l[0], l[1], int(l[2:])
        assert cond in '<>'

        start, end = val_ranges[var]
        assert start < val < end

        if cond == '>':
            fail_range, success_range = [start, val], [val + 1, end]
        else:
            success_range, fail_range = [start, val - 1], [val, end]

        s_val_ranges = {**val_ranges, var: success_range}
        f_val_ranges = {**val_ranges, var: fail_range}

        if wf == 'A':
            return get_combos(s_val_ranges) + get_step_combos(steps[1:], f_val_ranges)
        if wf == 'R':
            return get_step_combos(steps[1:], f_val_ranges)
        return get_step_combos(workflows[wf], s_val_ranges) + get_step_combos(steps[1:], f_val_ranges)

    print("Part 2:", get_step_combos(workflows['in'], {k: [1, 4000] for k in 'xmas'}))


if __name__ == "__main__":
    part1()
    part2()
