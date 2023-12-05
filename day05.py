from collections import defaultdict

from common import get_input


def get_maps(data):
    maps = defaultdict(list)
    map_name = None
    for line in data[1:]:
        if ":" in line:
            map_name = line.split(" map:")[0]
        elif line:
            dest_start, src_start, rng = map(int, line.split())
            maps[map_name].append((dest_start, src_start, rng))
    return maps


map_names = (
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
)


def part1():
    data = get_input(5)
    seed_nums = map(int, data[0].split(": ")[1].split())

    maps = get_maps(data)

    def map_val(map_name, src):
        for dest_start, src_start, rng in maps[map_name]:
            if src_start <= src < src_start + rng:
                return dest_start + (src - src_start)
        return src

    locs = []
    for seed in seed_nums:
        for map_name in map_names:
            seed = map_val(map_name, seed)
        locs.append(seed)
    print(min(locs))


def part2():
    data = get_input(5)
    seed_nums = list(map(int, data[0].split(": ")[1].split()))
    seed_pairs = []
    left = None
    for i, seed in enumerate(seed_nums):
        if i % 2 == 0:
            left = seed
        else:
            seed_pairs.append((left, left+seed-1))  # inclusive ranges

    # convert to inclusive ranges
    maps = get_maps(data)
    map_ranges = {
        mapping: [
            (src_start, src_start + rng - 1, dest_start, dest_start + rng - 1)
            for dest_start, src_start, rng in maps[mapping]
        ]
        for mapping in maps
    }

    for mapping in map_names:
        new_seed_pairs = []
        while seed_pairs:
            l, r = seed_pairs.pop(0)
            found = False
            for src_start, src_end, dest_start, dest_end in map_ranges[mapping]:
                if l > src_end or r < src_start:
                    continue

                if l < src_start:
                    seed_pairs.append((l, src_start - 1))
                    new_left = dest_start
                else:
                    new_left = dest_start+(l-src_start)

                if r > src_end:
                    seed_pairs.append((src_end + 1, r))
                    new_right = dest_end
                else:
                    new_right = dest_start+(r-src_start)

                new_seed_pairs.append((new_left, new_right))
                found = True
                break

            # not found to intersect
            if not found:
                new_seed_pairs.append((l, r))
        seed_pairs = new_seed_pairs
    print(min(pair[0] for pair in seed_pairs))


if __name__ == "__main__":
    part1()
    part2()
