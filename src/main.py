import sys

import pygame

from model.game import Game
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

screen = ScreenData(window)

clock = pygame.time.Clock()

game = Game(5, 5)
resource_holder.update_screen_data(screen, game)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.size
            resource_holder.update_screen_data(screen, game)

        if screen.get_screen_index() == 0:
            overview_screen.update(screen)
        else:
            play_screen.update(screen, game)

    pygame.display.flip()

    clock.tick(120)

pygame.quit()
sys.exit()
