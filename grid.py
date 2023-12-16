from enum import Enum
from typing import List, Tuple


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

    def display(self):
        print("\n".join("".join(row) for row in self.grid))


class Dirs(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


class GridEntity:
    def __init__(self, x, y, dir: Dirs):
        self.x = x
        self.y = y
        self.dir = dir
        
    def move(self, grid) -> bool:
        """Returns if still inside the grid"""
        match self.dir:
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
        match self.dir:
            case Dirs.N:
                self.dir = Dirs.E
            case Dirs.E:
                self.dir = Dirs.N
            case Dirs.S:
                self.dir = Dirs.W
            case Dirs.W:
                self.dir = Dirs.S

    def reflect_bw_slash(self):
        match self.dir:
            case Dirs.N:
                self.dir = Dirs.W
            case Dirs.E:
                self.dir = Dirs.S
            case Dirs.S:
                self.dir = Dirs.E
            case Dirs.W:
                self.dir = Dirs.N
                
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
