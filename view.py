import tkinter as tk
from tkinter import messagebox


class MenuView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Minesweeper Menu")

        self.label = tk.Label(self, text="Select Difficulty")
        self.label.pack(pady=10, padx=100)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        self.easy_but = tk.Button(self.button_frame, text="Easy", command=self.controller.start_easy, width=10)
        self.easy_but.grid(row=0, column=0, padx=5)

        self.hard_but = tk.Button(self.button_frame, text="Hard", command=self.controller.start_hard, width=10)
        self.hard_but.grid(row=0, column=1, padx=5)

        self.custom_but = tk.Button(self.button_frame, text="Custom", command=self.show_custom_settings, width=10)
        self.custom_but.grid(row=0, column=2, padx=5)

        self.custom_frame = tk.Frame(self)
        self.custom_frame.pack(pady=5)

        self.width_label = tk.Label(self.custom_frame, text="Width:")
        self.width_label.grid(row=0, column=0, padx=5)

        self.width_entry = tk.Entry(self.custom_frame)
        self.width_entry.grid(row=0, column=1, padx=5)

        self.height_label = tk.Label(self.custom_frame, text="Height:")
        self.height_label.grid(row=1, column=0, padx=5)

        self.height_entry = tk.Entry(self.custom_frame)
        self.height_entry.grid(row=1, column=1, padx=5)

        self.mines_label = tk.Label(self.custom_frame, text="Mines:")
        self.mines_label.grid(row=2, column=0, padx=5)

        self.mines_entry = tk.Entry(self.custom_frame)
        self.mines_entry.grid(row=2, column=1, padx=5)

        self.start_custom_but = tk.Button(self.custom_frame, text="Start custom", command=self.controller.start_custom)
        self.start_custom_but.grid(row=3, columnspan=2, pady=5)

        self.custom_entries = [self.width_entry, self.height_entry, self.mines_entry, self.start_custom_but,
                               self.width_label, self.height_label, self.mines_label]
        self.hide_custom_settings()

    def show_custom_settings(self):
        for widget in self.custom_entries:
            widget.grid()

    def hide_custom_settings(self):
        for widget in self.custom_entries:
            widget.grid_remove()

    def get_custom_settings(self):
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        mines = int(self.mines_entry.get())
        return width, height, mines


class GameView(tk.Toplevel):
    def __init__(self, controller, width, height, mines, model):
        super().__init__()
        self.model = model
        self.controller = controller
        self.paused = False
        self.title("Minesweeper Game")

        self.width = int(width)
        self.height = int(height)
        self.mines_amount = int(mines)

        self.timer_label = tk.Label(self, text="Time: 0:0")
        self.timer_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.pause_but = tk.Button(self, text="Pause", command=self.pause)
        self.pause_but.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.mines_label = tk.Label(self, text=f"Mines: {self.mines_amount}")
        self.mines_label.grid(row=1, column=0, padx=5, pady=5)

        self.flags_label = tk.Label(self, text="Flags: 0")
        self.flags_label.grid(row=1, column=1, padx=5, pady=5)

        self.board_frame = tk.Frame(self)
        self.board_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.pause_cover = tk.Canvas(self, bg="light grey", width=self.width*5, height=self.height*5)
        self.pause_cover.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.pause_cover.grid_forget()

        self.tiles = [[Tile(self.board_frame, row, col, self.controller, self.model)
                       for col in range(self.width)] for row in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col].grid(row=row, column=col)

    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_but.config(text="Continue")
            self.cover_board()
            self.controller.pause_time()
        else:
            self.paused = False
            self.pause_but.config(text="Pause")
            self.uncover_board()
            self.controller.resume_time()

    def cover_board(self):
        self.pause_cover.grid(row=2, column=0, columnspan=2, sticky="nsew")

    def uncover_board(self):
        self.pause_cover.grid_forget()

    def update_timer(self, time):
        minutes = time // 60
        seconds = time % 60
        self.timer_label.config(text=f"Time: {minutes}:{seconds}")

    def update_flags_label(self, flags):
        self.flags_label.config(text=f"Flags: {flags}")

    def congratulate(self, time):
        minutes = time // 60
        seconds = time % 60
        messagebox.showinfo("Congrats!", f"You won!\nTime: {minutes}:{seconds}")

    def you_lost(self):
        messagebox.showinfo("BOOM!", "You lost, better luck next time!")


class Tile(tk.Button):
    def __init__(self, master, row, col, controller, model):
        super().__init__(master, width=2, height=1, command=self.left_click)
        self.controller = controller
        self.model = model
        self.row = row
        self.col = col
        self.neighboring_mines = self.model.board[row][col]

        self.bind("<Button-3>", self.right_click)

    def left_click(self):
        self.controller.reveal_tile(self.row, self.col)

    def right_click(self, event):
        self.controller.place_flag(self.row, self.col)

    def set_flag(self):
        if (self.row, self.col) in self.controller.model.flags:
            self.config(text="🚩")
        else:
            self.config(text="")

    def reveal(self):
        if (self.row, self.col) in self.controller.model.mines:
            self.config(text="💣")
        else:
            self.config(text=str(self.neighboring_mines) if self.neighboring_mines > 0 else "")
        self.config(state="disabled")
