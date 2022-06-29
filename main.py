import pygame
from pygame.locals import QUIT
import sys
from gui import GameGui

pygame.init()
display = pygame.display.set_mode((550, 650))
pygame.display.set_caption("Sudoku")
FPS = pygame.time.Clock()
FPS.tick(60)

game_gui = GameGui(display)

game_gui.display_menu()

while True:
    pygame.display.update()
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            game_gui.get_click_location()
            if game_gui.on_menu_screen:
                game_gui.select_difficulty()
                game_gui.display_board()

        if event.type == pygame.KEYDOWN:
            if not game_gui.on_menu_screen:
                if event.key == 13:
                    game_gui.display_solved()
                if event.key == 32:
                    game_gui.display_hint()
                game_gui.input_player_entry(event.key)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
