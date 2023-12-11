def get_input(day, part=0):
    with open(f"inputs/{day:02}_{part}.txt") as f:
        lines = f.read().splitlines()
    return lines


def get_groups(data):
    curr_group = []
    groups = []
    for line in data:
        if not line:
            groups.append(curr_group)
            curr_group = []
        else:
            curr_group.append(line)
    groups.append(curr_group)
    return groups
