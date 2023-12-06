from common import get_input


def part1():
    data = get_input(6)
    times = list(map(int, data[0].split(":")[1].split()))
    distances = list(map(int, data[1].split(":")[1].split()))
    product = 1
    for i in range(len(times)):
        time = times[i]  # to hold & release
        dist = distances[i]  # to beat
        num_sols = 0
        for speed in range(time+1):
            time_left = time-speed
            full_dist = speed * time_left
            if full_dist > dist:
                num_sols += 1
        product *= num_sols
    print(product)



def part2():
    # todo: improve to use quadratic formula
    data = get_input(6)
    times = data[0].split(":")[1].split()
    time = int("".join(times))
    distances = data[1].split(":")[1].split()
    dist = int("".join(distances))
    num_sols = 0
    for speed in range(time + 1):
        time_left = time - speed
        full_dist = speed * time_left
        if full_dist > dist:
            num_sols += 1
    print(num_sols)


if __name__ == "__main__":
    part1()
    part2()
