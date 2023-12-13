class Grid:
    def __init__(self, data):
        """
        :param data: a 2-d list
        """
        self.grid = data
        self.width = len(data[0])
        self.height = len(data)

    def get_col(self, idx):
        return [row[idx] for row in self.grid]

    def get_row(self, idx):
        return self.grid[idx]
