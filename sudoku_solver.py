from enum import Enum

from sudoku import Sudoku


class SudokuState(Enum):
    the_end = 0
    need_for_random_shoot = 1
    error_in_random_shoot = 2


class SudokuSolver:
    def __init__(self, sudoku):
        self.stack = [sudoku, ]
        self.stack_random_shoot = []  # [(row, column), number, ]

    def solve(self):
        state = SudokuSolver.simple_solving(self.stack[-1])
        while state is not SudokuState.the_end:
            if state is SudokuState.need_for_random_shoot:
                # poszukaj pola z najmniejsza liczba mozliwosci
                current_sudoku = self.stack[-1]
                row, column = current_sudoku.find_cell_to_random_shoot()
                assert (len(current_sudoku.state_array[row][column]) > 0)
                # random shoot na row, column
                new_sudoku = Sudoku.from_sudoku(current_sudoku)
                number = new_sudoku.state_array[row][column][0]
                new_sudoku.fill_cell(row, column, number)
                self.stack_random_shoot.append(((row, column), number))
                self.stack.append(new_sudoku)
            elif state is SudokuState.error_in_random_shoot:
                assert (len(self.stack) > 1)  # nie przejmujemy sie nieprawidlowymi sudoku
                # wycofaj ostatni strzal
                self.stack.pop()
                (random_shoot_row, random_shoot_column), random_shoot_number = self.stack_random_shoot.pop()
                # poniewaz strzal byl bledny, mozemy wykreslic liczbe z mozliwosci z poprzedniego sudoku
                self.stack[-1].state_array[random_shoot_row][random_shoot_column].remove(random_shoot_number)
            # rozwiazuj dalej
            state = SudokuSolver.simple_solving(self.stack[-1])

        assert (state is SudokuState.the_end)
        assert (self.stack[-1].is_valid() and self.stack[-1].empty_fields is 0)
        return self.stack[-1]

    @staticmethod
    def simple_solving(sudoku):
        progress = 1
        assert(sudoku.is_valid())
        while progress > 0 and sudoku.is_valid():
            empty_fields = sudoku.empty_fields
            sudoku.naked_single()
            sudoku.hidden_single()
            progress = empty_fields - sudoku.empty_fields
        if sudoku.is_valid():
            if sudoku.empty_fields is 0:
                return SudokuState.the_end
            else:
                return SudokuState.need_for_random_shoot
        else:
            return SudokuState.error_in_random_shoot


def test_fill_state_array():
    path = './test/resources/grid'
    extension = '.txt'
    for i in range(1, 51):
        if i < 10:
            x = '0' + str(i)
        else:
            x = str(i)
        filename = path + x + extension
        solution = SudokuSolver(Sudoku.from_file(filename)).solve()
        assert(solution.is_valid())
        solution.print()

if __name__ == "__main__":
    test_fill_state_array()
