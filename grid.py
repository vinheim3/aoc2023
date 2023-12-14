from typing import List


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

    def get_row(self, idx: int) -> List[str]:
        return self.grid[idx]
