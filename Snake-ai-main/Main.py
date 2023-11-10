from GameGUI import GameGUI
import pygame
game = GameGUI()

while game.running:
    game.curr_menu.display_menu()
    game.game_loop()


