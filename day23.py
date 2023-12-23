import sys
from typing import List, Tuple

from common import get_input
from grid import Grid, get_offs

sys.setrecursionlimit(20_000)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connected: List[Tuple["Node", int]] = []  # tuples of other nodes, and distance to them


def get_connected_from_pos(grid: Grid, x, y, dx, dy, end_pos, part1):
    visited = {(x, y)}
    # Step to the next node
    x, y = x + dx, y + dy
    visited.add((x, y))
    steps = 1
    while 1:
        potential_next = set()
        for dx, dy in get_offs():
            (sx, sy) = new_pos = x + dx, y + dy
            if new_pos == end_pos:
                return steps + 1, new_pos
            if new_pos in visited:
                continue
            ch = grid.cell(sx, sy)
            if ch == '#':
                continue

            if part1 and (
                (dx == -1 and ch == '>') or
                (dx == 1 and ch == '<') or
                (dy == -1 and ch == 'v') or
                (dy == 1 and ch == '^')
            ):
                continue
            potential_next.add(new_pos)
        if len(potential_next) == 0:  # No valid paths due to slopes
            return None
        elif len(potential_next) == 1:  # Keep moving along this path
            steps += 1
            x, y = potential_next.pop()
            visited.add((x, y))
        else:
            return steps, (x, y)  # Return the new graph node and distance to it


def get_longest_path(visited, node: Node, last_node: Node):
    if node == last_node:
        return 0
    paths = [
        steps + get_longest_path({*visited, on}, on, last_node)
        for on, steps in node.connected if on not in visited
    ]
    return max(paths) if paths else -1_000_000


def run(part1):
    grid = Grid(get_input(23))
    paths = grid.find_chs('.')
    start_pos = [pos for pos in paths if pos[1] == 0][0]
    end_pos = [pos for pos in paths if pos[1] == grid.height-1][0]

    graph = {start_pos: Node(*start_pos)}

    to_expand_from = {start_pos}
    while to_expand_from:
        (ox, oy) = to_expand_from.pop()
        connected = []
        for dx, dy in get_offs():
            sx, sy = ox + dx, oy + dy
            if not (0 <= sx < grid.width and 0 <= sy < grid.height):
                continue
            if grid.cell(sx, sy) == '#':
                continue
            ret = get_connected_from_pos(grid, ox, oy, dx, dy, end_pos, part1)
            if ret is None:
                continue
            steps, (x, y) = ret
            if (x, y) not in graph:
                graph[(x, y)] = Node(x, y)
                to_expand_from.add((x, y))
            connected.append((graph[(x, y)], steps))
        graph[(ox, oy)].connected = connected

    start = graph[start_pos]
    return get_longest_path({start}, start, graph[end_pos])


if __name__ == "__main__":
    print("Part 1:", run(True))
    print("Part 2:", run(False))
