def get_input(day, part=0):
    with open(f"inputs/{day:02}_{part}.txt") as f:
        lines = f.read().splitlines()
    return lines
