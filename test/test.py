import unittest
from mock import MagicMock
from sudoku import Sudoku


class SudokuTest(unittest.TestCase):
    @staticmethod
    def create_sudoku_array(string):
        return [[int(string[9 * j + i]) for i in range(9)] for j in range(9)]

    def test_init(self):
        array = SudokuTest.create_sudoku_array(
            "300200000000107000706030500070009080900020004010800050009040301000702000000008006")
        sudoku = Sudoku(array)
        for i in range(9):
            for j in range(9):
                self.assertEqual(array[i][j], sudoku.array[i][j])

    def test_from_file(self):
        array = SudokuTest.create_sudoku_array(
            "300200000000107000706030500070009080900020004010800050009040301000702000000008006")
        sudoku = Sudoku.from_file('./resources/grid01.txt')
        for i in range(9):
            for j in range(9):
                self.assertEqual(array[i][j], sudoku.array[i][j])

    def test_from_sudoku(self):
        array = SudokuTest.create_sudoku_array(
            "300200000000107000706030500070009080900020004010800050009040301000702000000008006")
        sudoku1 = Sudoku(array)
        sudoku2 = Sudoku.from_sudoku(sudoku1)
        for i in range(9):
            for j in range(9):
                self.assertEqual(sudoku1.array[i][j], sudoku2.array[i][j])
                self.assertEqual(sudoku1.state_array[i][j], sudoku2.state_array[i][j])

    def test_get_square_coordinates(self):
        for i in range(0, 3):
            self.assertEqual(Sudoku.get_square_coordinates(i), 0)
        for i in range(3, 6):
            self.assertEqual(Sudoku.get_square_coordinates(i), 3)
        for i in range(6, 9):
            self.assertEqual(Sudoku.get_square_coordinates(i), 6)

    def test_all_possibilities(self):
        array = Sudoku.all_possibilities()
        for i in range(1, 10):
            self.assertIn(i, array)

    def fill_state_array_simple_test(self, filename):
        sudoku = Sudoku.from_file(filename)
        for row in range(9):
            for column in range(9):
                if sudoku.array[row][column] is 0:
                    self.assertTrue(len(sudoku.state_array[row][column]) == 0)
                else:
                    # row
                    for x in range(9):
                        if x is not row:
                            self.assertNotEqual(sudoku.array[x][column], sudoku.array[row][column])
                            self.assertNotIn(sudoku.array[row][column], sudoku.state_array[x][column])
                    # column
                    for y in range(9):
                        if y is not column:
                            self.assertNotEqual(sudoku.array[row][y], sudoku.array[row][column])
                            self.assertNotIn(sudoku.array[row][column], sudoku.state_array[row][y])

                    # square
                    square_x, square_y = Sudoku.get_square_coordinates(row), Sudoku.get_square_coordinates(column)
                    for x in range(square_x, square_x + 3):
                        for y in range(square_y, square_y + 3):
                            if x is not row or y is not column:
                                self.assertNotEqual(sudoku.array[x][y], sudoku.array[row][column])
                                self.assertNotIn(sudoku.array[row][column], sudoku.state_array[x][y])

    def test_fill_state_array(self):
        path = './resources/grid'
        extension = '.txt'
        for i in range(1, 51):
            if i < 10:
                x = '0' + str(i)
            else:
                x = str(i)
            filename = path + x + extension
            self.fill_state_array_simple_test(filename)


if __name__ == '__main__':
    unittest.main()
