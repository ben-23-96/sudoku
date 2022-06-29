import requests
import copy


class Sudoku():
    def __init__(self):
        self.unsolved_puzzle = []
        self.solved_puzzle = []

    def generate_sudoku_puzzle(self, difficulty):
        response = requests.get(
            f"https://sugoku.herokuapp.com/board?difficulty={difficulty}")
        self.unsolved_puzzle = response.json()['board']
        self.solved_puzzle = copy.deepcopy(self.unsolved_puzzle)
        solve_puzzle = self.solve(0, 0)

    def solve(self, row, col):
        if row == 8 and col == 9:
            return True

        if col == 9:
            col = 0
            row += 1

        if self.solved_puzzle[row][col] > 0:
            return self.solve(row, col+1)

        for num in range(1, 10):

            if self.check(row, col, num):
                self.solved_puzzle[row][col] = num

                if self.solve(row, col+1):
                    return True

            self.solved_puzzle[row][col] = 0

        return False

    def check(self, row, col, number):
        if number in self.solved_puzzle[row]:
            return False

        if number in list(zip(*self.solved_puzzle))[col]:
            return False

        if row < 3:
            row_slct = [0, 1, 2]
        if row >= 3 and row < 6:
            row_slct = [3, 4, 5]
        if row >= 6 and row < 9:
            row_slct = [6, 7, 8]

        if col < 3:
            col_slct = [0, 3]
        if col >= 3 and col < 6:
            col_slct = [3, 6]
        if col >= 6 and col < 9:
            col_slct = [6, 9]

        if number in self.solved_puzzle[row_slct[0]][col_slct[0]:col_slct[1]] or number in self.solved_puzzle[row_slct[1]][col_slct[0]:col_slct[1]] or number in self.solved_puzzle[row_slct[2]][col_slct[0]:col_slct[1]]:
            return False

        return True
