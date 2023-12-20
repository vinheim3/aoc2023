from enum import Enum
from typing import List, Tuple, Optional, Dict

from common import make_md_array


class Grid:
    def __init__(self, data):
        """
        :param data: a 2-d list
        """
        self.grid = [[*row] for row in data]
        self.width = len(data[0])
        self.height = len(data)

    def cell(self, x, y):
        return self.grid[y][x]

    def get_col(self, idx: int) -> List[str]:
        return [row[idx] for row in self.grid]

    def get_cols(self):
        for i in range(self.width):
            yield self.get_col(i)

    def get_row(self, idx: int) -> List[str]:
        return self.grid[idx]

    def get_rows(self):
        for i in range(self.height):
            yield self.get_row(i)

    def set_col(self, idx: int, col: List[str]):
        for i in range(self.height):
            self.grid[i][idx] = col[i]

    def set_row(self, idx: int, row: List[str]):
        self.grid[idx] = row

    def find_chs(self, ch) -> List[Tuple[int, int]]:
        ret = []
        for rowi, row in enumerate(self.get_rows()):
            for coli, cell in enumerate(row):
                if cell == ch:
                    ret.append((coli, rowi))
        return ret

    def find_ch(self, ch) -> Tuple[int, int]:
        ret = self.find_chs(ch)
        assert len(ret) == 1
        return ret[0]

    def display(self, metadata: Optional[Dict[int, str]] = None):
        if not metadata:
            print("\n".join("".join(row) for row in self.grid))
        else:
            for i, row in enumerate(self.get_rows()):
                print("".join(row) + " " + metadata.get(i, ""))

    def to_immutable(self):
        return tuple(tuple(row) for row in self.grid)

    def flipx(self):
        return Grid(make_md_array(self.width, self.height, lambda c, r: self.cell(self.width-c-1, r)))

    def rotateCW(self):
        return Grid(make_md_array(self.width, self.height, lambda c, r: self.cell(r, self.width-c-1)))

    def astar(self, x, y, tx, ty):
        _, grid_parents, _ = self.astar_expand(x, y, walls={'#'}, floors={'.'}, targets=set())
        return self.astar_move(x, y, tx, ty, grid_parents)

    def astar_expand(self, _x, _y, walls: set, floors: set, targets: set):
        grid_vals = make_md_array(self.width, self.height, lambda c, r: -1)
        grid_parents: List[List[List[Tuple[int, int]]]] = make_md_array(self.width, self.height, lambda c, r: list())
        grid_vals[_y][_x] = 0
        dist = 1

        # Init for curr square
        squares_done = {(_x, _y)}
        squares_to_consider = set(get_surrounding(_x, _y))
        for x, y in squares_to_consider:
            grid_parents[y][x].append((_x, _y))

        reachable_targets = set()
        while squares_to_consider:
            new_to_consider = set()
            for x, y in squares_to_consider:
                squares_done.add((x, y))
                if 0 <= x < self.width and 0 <= y < self.height:
                    if self.cell(x, y) in floors:
                        grid_vals[y][x] = dist
                        for coords in get_surrounding(x, y):
                            childx, childy = coords
                            if self.cell(childx, childy) in walls:
                                continue
                            parent_details = grid_parents[childy][childx]
                            if parent_details:
                                px, py = parent_details[0]
                                if grid_vals[py][px] == dist and (x, y) not in parent_details:
                                    parent_details.append((x, y))
                            else:
                                parent_details.append((x, y))
                            if coords not in squares_done:
                                new_to_consider.add(coords)
                        if (x, y) in targets:
                            reachable_targets.add((x, y))
            squares_to_consider = new_to_consider
            dist += 1
        grid_parents[_y][_x] = []
        return grid_vals, grid_parents, reachable_targets

    @staticmethod
    def astar_move(x, y, targetx, targety, grid_parents):
        currx, curry = targetx, targety
        path = []
        while currx != x or curry != y:
            parents = grid_parents[curry][currx]
            prevx, prevy = currx, curry
            currx, curry = get_1st_reading_order_coord(parents)
            path.insert(0, (prevx, prevy))
        return path


def get_surrounding(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def get_surrounding_with_dirs(x, y):
    return [(x - 1, y, Dirs.W), (x + 1, y, Dirs.E), (x, y - 1, Dirs.N), (x, y + 1, Dirs.S)]


def get_offs_with_dirs(x, y):
    return [(-1, 0, Dirs.W), (1, 0, Dirs.E), (0, -1, Dirs.N), (0, 1, Dirs.S)]


def get_1st_reading_order_coord(coords):
    min_x = min_y = 1_000
    for x, y in coords:
        if y < min_y:
            min_x = x
            min_y = y
        elif y == min_y and x < min_x:
            min_x = x
    return min_x, min_y


class Dirs(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


class GridEntity:
    def __init__(self, x, y, dir_: Dirs):
        self.x = x
        self.y = y
        self.dir_ = dir_
        
    def move(self, grid) -> bool:
        """Returns if still inside the grid"""
        match self.dir_:
            case Dirs.N:
                self.y -= 1
                if self.y < 0:
                    return False
            case Dirs.E:
                self.x += 1
                if self.x == grid.width:
                    return False
            case Dirs.S:
                self.y += 1
                if self.y == grid.height:
                    return False
            case Dirs.W:
                self.x -= 1
                if self.x < 0:
                    return False

        return True
    
    def reflect_fw_slash(self):
        match self.dir_:
            case Dirs.N:
                self.dir_ = Dirs.E
            case Dirs.E:
                self.dir_ = Dirs.N
            case Dirs.S:
                self.dir_ = Dirs.W
            case Dirs.W:
                self.dir_ = Dirs.S

    def reflect_bw_slash(self):
        match self.dir_:
            case Dirs.N:
                self.dir_ = Dirs.W
            case Dirs.E:
                self.dir_ = Dirs.S
            case Dirs.S:
                self.dir_ = Dirs.E
            case Dirs.W:
                self.dir_ = Dirs.N

    def split_vert(self):
        return [
            GridEntity(self.x, self.y, Dirs.N),
            GridEntity(self.x, self.y, Dirs.S),
        ]

    def split_horiz(self):
        return [
            GridEntity(self.x, self.y, Dirs.E),
            GridEntity(self.x, self.y, Dirs.W),
        ]
