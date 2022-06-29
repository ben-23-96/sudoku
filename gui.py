import pygame
from sudoku_generator import Sudoku


class GameGui():
    def __init__(self, display):
        self.display = display
        self.colours = {'blue': (0, 0, 255),
                        'red': (255, 0, 0),
                        'green': (0, 255, 0),
                        'black': (0, 0, 0),
                        'white': (255, 255, 255),
                        'purple': (125, 38, 205)}
        self.font_small = pygame.font.SysFont(
            "comic sans", size=15, bold=False, italic=False)
        self.font_medium = pygame.font.SysFont(
            "comic sans", size=30, bold=True, italic=False)
        self.font_large = pygame.font.SysFont(
            "comic sans", size=60, bold=True, italic=False)
        self.original_indexes = []
        self.input_indexes = []
        self.i = 0
        self.j = 0
        self.on_menu_screen = True
        self.showing_hint = False
        self.game_complete = False
        self.difficulty = "easy"
        self.sudoku = Sudoku()

    def display_menu(self):
        self.on_menu_screen = True

        pygame.draw.rect(self.display, self.colours['white'], (0, 0, 550, 650))

        self.write(2, 1.6, self.colours['blue'], "SUDOKU", self.font_large)

        text_easy = self.font_small.render(
            "EASY", True, self.colours['green'])
        self.display.blit(text_easy, (80, 415))
        text_medium = self.font_small.render(
            "MEDIUM", True, self.colours['blue'])
        self.display.blit(text_medium, (242, 415))
        text_hard = self.font_small.render("HARD", True, self.colours['red'])
        self.display.blit(text_hard, (430, 415))

        pygame.draw.rect(
            self.display, self.colours['black'], (50, 400, 100, 50), 2)
        pygame.draw.rect(
            self.display, self.colours['black'], (225, 400, 100, 50), 2)
        pygame.draw.rect(
            self.display, self.colours['black'], (400, 400, 100, 50), 2)

    def get_click_location(self):
        pos = pygame.mouse.get_pos()
        self.i, self.j = (pos[1]//50)-1, (pos[0]//50)-1

    def select_difficulty(self):
        #pos = pygame.mouse.get_pos()
        #i, j = (pos[1]//50)-1, (pos[0]//50)-1
        # if self.on_menu_screen:
        if (self.j == 0 or self.j == 1) and self.i == 7:
            self.difficulty = 'easy'
        if (self.j == 3 or self.j == 4) and self.i == 7:
            self.difficulty = 'medium'
        if (self.j == 7 or self.j == 8) and self.i == 7:
            self.difficulty = 'hard'

    def display_board(self):
        count_column = 0
        count_row = 0
        x = 50
        y = 50

        self.on_menu_screen = False
        self.sudoku.generate_sudoku_puzzle(self.difficulty)

        pygame.draw.rect(self.display, self.colours['white'], (0, 0, 550, 550))

        for i in range(1, 12, 3):
            pygame.draw.line(
                self.display, self.colours['black'], (50*i, 50), (50*i, 500), 6)
            pygame.draw.line(
                self.display, self.colours['black'], (50, 50*i), (500, 50*i), 6)

        for i in range(81):
            pygame.draw.rect(
                self.display, self.colours['black'], (x, y, 50, 50), 2)
            count_column += 1
            x += 50
            if count_column == 9:
                count_row += 1
                count_column = 0
                x = 50
                y += 50

        for i in range(9):
            for j in range(9):
                if self.sudoku.unsolved_puzzle[i][j] != 0:
                    self.original_indexes.append((i, j))
                    number = self.font_medium.render(
                        str(self.sudoku.unsolved_puzzle[i][j]), True, self.colours['black'])
                    self.display.blit(number, ((j*50+65), (i*50+55)))

        self.write(9.25, 0.9, self.colours['blue'],
                   "toggle hint with SPACE", self.font_medium)
        self.write(10.5, 1.9, self.colours['blue'],
                   "solve with ENTER", self.font_medium)

    def write(self, i, j, colour, input, font):
        text = font.render(input, True, colour)
        self.display.blit(text, (((j)*50+65), ((i)*50+55)))

    def delete_num(self, i, j):
        pygame.draw.rect(
            self.display, self.colours['white'], (((j)*50+60), ((i)*50+60), 30, 30))

    def input_player_entry(self, entry):
        if self.i < 0 or self.i > 8 or self.j < 0 or self.j > 8 or entry < 49 or entry > 57:  # faulty inputs #
            return None

        # original puzzle numbers #
        if self.sudoku.unsolved_puzzle[self.i][self.j] != 0 and (self.i, self.j) not in self.input_indexes:
            return None

        if self.sudoku.unsolved_puzzle[self.i][self.j] == 0:     # write #
            self.write(self.i, self.j, self.colours['blue'], str(
                entry-48), self.font_medium)
            self.sudoku.unsolved_puzzle[self.i][self.j] = entry - 48
            self.input_indexes.append((self.i, self.j))
            return None

        if (self.i, self.j) in self.input_indexes:    # overwrite #
            self.delete_num(self.i, self.j)
            self.write(self.i, self.j, self.colours['blue'], str(
                entry-48), self.font_medium)
            self.sudoku.unsolved_puzzle[self.i][self.j] = entry - 48

    def display_solved(self):
        if self.game_complete:
            self.display_menu()
            self.game_complete = False
            return None
        for i in range(9):
            for j in range(9):
                if self.sudoku.unsolved_puzzle[i][j] == self.sudoku.solved_puzzle[i][j] and (i, j) not in self.original_indexes:
                    self.delete_num(i, j)
                    self.write(i, j, self.colours['green'], str(
                        self.sudoku.solved_puzzle[i][j]), self.font_medium)
                if self.sudoku.unsolved_puzzle[i][j] != self.sudoku.solved_puzzle[i][j] and (i, j) not in self.original_indexes:
                    self.delete_num(i, j)
                    self.write(i, j, self.colours['purple'],
                               str(self.sudoku.solved_puzzle[i][j]), self.font_medium)
                    if self.sudoku.unsolved_puzzle[i][j] != 0:
                        self.write(i+0.4, j+0.4, self.colours['red'],
                                   str(self.sudoku.unsolved_puzzle[i][j]), self.font_small)

        if self.sudoku.unsolved_puzzle == self.sudoku.solved_puzzle:
            pygame.draw.rect(self.colours['white'], (0, 520, 500, 150))
            self.write(9.5, 0, self.colours['green'], "winner winner chicken dinner",
                       self.font_medium)
            self.write(10.5, 0, self.colours['blue'],
                       "press ENTER for new game", self.font_medium)

        if self.sudoku.unsolved_puzzle != self.sudoku.solved_puzzle:
            pygame.draw.rect(
                self.display, self.colours['white'], (0, 520, 500, 150))
            self.write(9.5, 1, self.colours['red'], "better luck next time",
                       self.font_medium)
            self.write(10.5, 0, self.colours['blue'],
                       "press ENTER for new game", self.font_medium)
        self.game_complete = True
        self.reset()

    def display_hint(self):

        if not self.showing_hint:
            for i, j in self.input_indexes:
                if self.sudoku.unsolved_puzzle[i][j] != self.sudoku.solved_puzzle[i][j]:
                    self.delete_num(i, j)
                    self.write(i, j, self.colours['red'], str(
                        self.sudoku.unsolved_puzzle[i][j]), self.font_medium)
                if self.sudoku.unsolved_puzzle[i][j] == self.sudoku.solved_puzzle[i][j]:
                    self.delete_num(i, j)
                    self.write(i, j, self.colours['green'], str(
                        self.sudoku.unsolved_puzzle[i][j]), self.font_medium)
            self.showing_hint = True
            return None
        if self.showing_hint:
            for i, j in self.input_indexes:
                self.delete_num(i, j)
                self.write(i, j, self.colours['blue'], str(
                    self.sudoku.unsolved_puzzle[i][j]), self.font_medium)
            self.showing_hint = False

    def reset(self):
        self.original_indexes = []
        self.input_indexes = []
        self.i = 0
        self.j = 0
        self.showing_hint = False
