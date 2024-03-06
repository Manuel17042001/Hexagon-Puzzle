import sys

import pygame

from model.game_manager import GameManager
from model.screen_data import ScreenData
from screens import play_screen, overview_screen
from utils import resource_holder

pygame.init()

window_width = 3000
window_height = 2000
window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
pygame.display.set_caption("Hexagonal Puzzle")
pygame.display.set_icon(resource_holder.image_icon)

running = True

screen = ScreenData()
screen.initialize(window)

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.size
            if GameManager().get_game():
                resource_holder.update_screen_data(ScreenData(), GameManager().get_game().get_map().get_grid_size())

    if screen.get_screen_index() == 0:
        overview_screen.update()
    else:
        play_screen.update()

    pygame.display.flip()

    clock.tick(120)

pygame.quit()
sys.exit()
