from view import MenuView, GameView
from model import Model


class Controller:
    def __init__(self):
        self.menu_view = MenuView(self)
        self.game_view = None
        self.model = None
        self.timer = 0
        self.timer_running = False

    def pause_time(self):
        self.timer_running = False

    def resume_time(self):
        self.timer_running = True
        self.update_timer()

    def start_easy(self):
        width, height, mines = 6, 6, 6
        self.start_game(width, height, mines)

    def start_hard(self):
        width, height, mines = 10, 10, 32
        self.start_game(width, height, mines)

    def start_custom(self):
        width, height, mines = self.menu_view.get_custom_settings()
        self.start_game(width, height, mines)

    def start_game(self, width, height, mines):
        self.model = Model(width, height, mines)
        self.game_view = GameView(self, width, height, mines, self.model)
        self.timer = 0
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer += 1
            self.game_view.update_timer(self.timer)
            self.menu_view.after(1000, self.update_timer)

    def place_flag(self, row, col):
        if (row, col) not in self.model.revealed:
            self.model.place_flag_m(row, col)
            self.game_view.tiles[row][col].set_flag()
            self.game_view.update_flags_label(len(self.model.flags))

    def reveal_tile(self, row, col):
        if (row, col) not in self.model.revealed and (row, col) not in self.model.flags:
            if self.model.check_loss(row, col):
                self.reveal_all()
                self.timer_running = False
                self.game_view.you_lost()
            self.model.reveal_tile_m(row, col)
            tile = self.game_view.tiles[row][col]
            tile.reveal()
            if tile.neighboring_mines == 0:
                tile.config(bg="light grey")
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if 0 <= r < len(self.model.board) and 0 <= c < len(self.model.board[0])\
                                and (r, c) not in self.model.revealed:
                            self.reveal_tile(r, c)
            if self.model.check_win():
                self.timer_running = False
                self.game_view.congratulate(self.timer)

    def reveal_all(self):
        for row in self.game_view.tiles:
            for tile in row:
                tile.reveal()


if __name__ == "__main__":
    app = Controller()
    app.menu_view.mainloop()
