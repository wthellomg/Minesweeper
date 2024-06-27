import random


class Model:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines_amount = mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.mines = set()
        self.flags = set()
        self.revealed = set()
        self._place_mines()

    def _place_mines(self):
        while len(self.mines) < self.mines_amount:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                self.board[row][col] = -1
                self._increment_neighbors(row, col)

    def _increment_neighbors(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.height and 0 <= c < self.width and self.board[r][c] != -1:
                    self.board[r][c] += 1

    def reveal_tile_m(self, row, col):
        self.revealed.add((row, col))

    def place_flag_m(self, row, col):
        if (row, col) in self.flags:
            self.flags.remove((row, col))
        else:
            self.flags.add((row, col))

    def check_win(self):
        return len(self.revealed) == self.width * self.height - self.mines_amount

    def check_loss(self, row, col):
        return (row, col) in self.mines
