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
