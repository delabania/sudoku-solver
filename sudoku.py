class Sudoku:
    def __init__(self, array):
        """
        :param table: two-dimensional list (9x9) of numbers - 0 for blank cell, 1-9 for filled cell
        """
        self.array = array
        self.state_array = [[[] for column in range(9)] for row in range(9)]
        self.fill_state_array()
        self.empty_fields = self.count_empty_fields()

    @classmethod
    def from_file(cls, filename):
        """
        :param filename: name of file which contains sudoku in specific format
        :return: new sudoku object
        """
        rows = open(filename, 'r').read().split('\n')
        array = [[int(rows[row][column]) for column in range(9)] for row in range(9)]
        return cls(array)

    @classmethod
    def from_sudoku(cls, sudoku):
        return cls(sudoku.array)

    @staticmethod
    def get_square_coordinates(coordinate):
        return coordinate - coordinate % 3

    @staticmethod
    def all_possibilities():
        return [n for n in range(1, 10)]

    def fill_state_array(self):
        for row in range(9):
            for column in range(9):
                if self.array is 0:
                    self.state_array[row][column] = Sudoku.all_possibilities()
                else:
                    self.state_array[row][column] = []
        for row in range(9):
            for column in range(9):
                if self.array[row][column] is not 0:
                    self.update_sudoku_state_array(row, column, self.array[row][column])

    def update_cell_state(self, row, column, number):
        if self.array[row][column] is 0 and number in self.state_array[row][column]:
            self.state_array[row][column].remove(number)

    def update_square(self, square_x, square_y, number):
        for row in range(square_x, square_x + 3):
            for column in range(square_y, square_y + 3):
                self.update_cell_state(row, column, number)

    def update_row(self, row, number):
        for column in range(9):
            self.update_cell_state(row, column, number)

    def update_column(self, column, number):
        for row in range(9):
            self.update_cell_state(row, column, number)

    def update_sudoku_state_array(self, row, column, number):
        assert (number is not 0)
        self.update_square(Sudoku.get_square_coordinates(row), Sudoku.get_square_coordinates(column), number)
        self.update_row(row, number)
        self.update_column(column, number)

    def fill_cell(self, row, column, number):
        assert (number in self.state_array[row][column])
        self.array[row][column] = number
        self.update_sudoku_state_array(row, column, number)
        self.empty_fields -= 1

    def count_empty_fields(self):
        counter = 0
        for row in range(9):
            for column in range(9):
                if self.array[row][column] is 0:
                    counter += 1
        return counter

    def is_valid(self, x, y):
        number = self.state_array[x][y]
        for column in range(9):
            if column is not y:
                if self.state_array[x][column] is number:
                    return False
        for row in range(9):
            if row is not x:
                if self.state_array[row][y] is number:
                    return False
        square_row, square_column = Sudoku.get_square_coordinates(x), Sudoku.get_square_coordinates(y)
        for i in range(square_row, square_row + 3):
            for j in range(square_column, square_column + 3):
                if i is not x and j is not y and self.state_array[i][j] is number:
                    return False
        return True

    #metody rozwiazywania
    def naked_single(self):
        for row in range(9):
            for column in range(9):
                if len(self.state_array[row][column]) is 1 and self.array[row][column] is 0:
                    self.fill_cell(row, column, self.state_array[row][column][0])

    def hidden_single(self):
        pass


s = Sudoku.from_file('./test/resources/grid01.txt')
print(s.array[7][0])
k = Sudoku.from_sudoku(s)
print(k.array[7][0])
