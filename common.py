from typing import Callable, List, TypeVar


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


T = TypeVar("T")


def make_md_array(width, height, f: Callable[[int, int], T]) -> List[List[T]]:
    arr = []
    for ri in range(height):
        row = []
        for ci in range(width):
            row.append(f(ci, ri))
        arr.append(row)
    return arr


def group_by(arr, num):
    groups = []
    curr_group = []
    for entry in arr:
        curr_group.append(entry)
        if len(curr_group) == num:
            groups.append(curr_group)
            curr_group = []
    if len(curr_group) == num:
        groups.append(curr_group)
    return groups


def nums(string) -> List[int]:
    return list(map(int, string.split()))


class LLNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

    def forward(self, num):
        curr = self
        for _ in range(num):
            curr = curr.next
        return curr
