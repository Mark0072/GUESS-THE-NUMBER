import tkinter as tk
from tkinter import messagebox
import random

class Sudoku:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Game")

        self.grid = [[0] * 9 for _ in range(9)]
        self.create_grid()
        self.generate_sudoku()

        self.solve_button = tk.Button(master, text="Check Solution", command=self.check_solution)
        self.solve_button.grid(row=10, column=0, columnspan=9)

    def create_grid(self):
        self.entries = [[None] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                frame = tk.Frame(self.master, width=50, height=50)
                frame.grid(row=i, column=j, padx=1, pady=1)
                frame.grid_propagate(False)
                self.entries[i][j] = tk.Entry(frame, font=('Arial', 18), width=2, justify='center')
                self.entries[i][j].pack(expand=True, fill='both')

    def generate_sudoku(self):
        # Simple Sudoku generator (not a full generator, just for demonstration)
        numbers = list(range(1, 10))
        for i in range(9):
            random.shuffle(numbers)
            for j in range(9):
                if random.random() < 0.5:  # Randomly fill some cells
                    self.entries[i][j].insert(0, str(numbers[j]))

    def check_solution(self):
        try:
            user_grid = [[int(self.entries[i][j].get() or 0) for j in range(9)] for i in range(9)]
            if self.is_valid_sudoku(user_grid):
                messagebox.showinfo("Sudoku", "Congratulations! You solved the Sudoku!")
            else:
                messagebox.showerror("Sudoku", "Incorrect solution. Try again!")
        except ValueError:
            messagebox.showerror("Sudoku", "Please enter valid numbers.")

    def is_valid_sudoku(self, board):
        # Check rows, columns, and 3x3 boxes
        for i in range(9):
            if not self.is_valid_unit(board[i]):
                return False
            if not self.is_valid_unit([board[j][i] for j in range(9)]):
                return False

        for i in range(3):
            for j in range(3):
                if not self.is_valid_unit([board[x][y] for x in range(i * 3, i * 3 + 3) for y in range(j * 3, j * 3 + 3)]):
                    return False

        return True

    def is_valid_unit(self, unit):
        unit = [num for num in unit if num != 0]
        return len(unit) == len(set(unit))

if __name__ == "__main__":
    root = tk.Tk()
    sudoku_game = Sudoku(root)
    root.mainloop()