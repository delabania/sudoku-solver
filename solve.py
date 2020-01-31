from argparse import ArgumentParser

from sudoku_solver import SudokuSolver
from sudoku import Sudoku

def get_args():
    parser = ArgumentParser()
    parser.add_argument('--sudoku', required=True)

    return parser.parse_args()

def main():
    args = get_args()
    sudoku = Sudoku.from_file(args.sudoku)
    solver = SudokuSolver(sudoku)
    solved_sudoku = solver.solve()
    solved_sudoku.print_sudoku()

if __name__ == '__main__':
    main()