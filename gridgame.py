class GameObject:
    def __init__(self, symbol, row, col):
        self.symbol = symbol
        self.row = row
        self.col = col

    def print_object(self):
        print(self.symbol, self.row + 1, self.col + 1)


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append("-")
            self.board.append(row)

    def display(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def place_object(self, obj):
        self.board[obj.row][obj.col] = obj.symbol

    def move_object(self, obj, new_row, new_col):
        new_row = max(0, min(new_row, self.rows - 1))
        new_col = max(0, min(new_col, self.cols - 1))
        self.board[obj.row][obj.col] = "-"
        obj.row = new_row
        obj.col = new_col
        self.place_object(obj)


grid = Grid(10, 10)

row_inp = int(input("Masukkan row awal hero (1-10): "))
col_inp = int(input("Masukkan col awal hero (1-10): "))

row = max(0, min(row_inp - 1, grid.rows - 1))
col = max(0, min(col_inp - 1, grid.cols - 1))


hero = GameObject("Z", row, col)
grid.place_object(hero)
grid.display()

while True:
    print("Masukkan koordinat baru hero (1-10) atau ketik x untuk keluar")

    new_row_inp = input("Row baru: ")
    if new_row_inp == "x":
        break
    else:
        new_row_input = int(new_row_inp)

    new_col_input = int(input("Col baru: "))

    new_row = new_row_input - 1
    new_col = new_col_input - 1

    grid.move_object(hero, new_row, new_col)
    grid.display()