from common import get_input


def hsh(string):
    cv = 0
    for ch in string:
        cv = ((cv + ord(ch)) * 17) % 256
    return cv


if __name__ == "__main__":
    data = get_input(15)[0].split(",")

    print("Part 1:", sum(hsh(entry) for entry in data))

    boxes = [{} for _ in range(256)]
    for entry in data:
        if entry.endswith("-"):
            label = entry[:-1]
            box = hsh(label)
            if label in boxes[box]:
                del boxes[box][label]
        else:
            label, val = entry.split('=')
            boxes[hsh(label)][label] = int(val)

    print("Part 2:", sum(
        sum((i + 1) * (j + 1) * val for j, val in enumerate(box.values()))
        for i, box in enumerate(boxes)
    ))
