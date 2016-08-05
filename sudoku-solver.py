class SudokuSolver:
    def __init__(self, sudoku):
        self.stack = sudoku
        self.level = [[0 for column in range(9)] for row in range(9)]

    def solve(self):
        pass

