from typing import List, Callable


class Grid:
    def __init__(self, data):
        """
        :param data: a 2-d list
        """
        self.grid = [[*row] for row in data]
        self.width = len(data[0])
        self.height = len(data)

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
