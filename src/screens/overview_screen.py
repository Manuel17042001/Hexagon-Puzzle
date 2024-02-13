import math
import sys

import pygame

from model.screen_data import ScreenData
from utils import resource_holder


def update(screen_data: ScreenData) -> None:
    window = screen_data.get_window()
    width = window.get_width()
    height = window.get_height()

    background_image = resource_holder.image_background_start_screen
    background_image = pygame.transform.scale(background_image, (width, height))
    window.blit(background_image, (0, 0))

    hexagon_image = resource_holder.image_hexagon_start_screen
    hexagon_image = pygame.transform.scale(hexagon_image, (height * 0.7, height * .7))
    window.blit(hexagon_image, (width - hexagon_image.get_width() / 4 * 2.5, -hexagon_image.get_height() * .1))

    hexagon_image = pygame.transform.scale(hexagon_image, (height * .5, height * .5))
    window.blit(hexagon_image, (-hexagon_image.get_width() * .2, -hexagon_image.get_height() * .1))

    hexagon_image = pygame.transform.scale(hexagon_image, (height * .25, height * .25))
    window.blit(hexagon_image, (hexagon_image.get_width() * 0.8, hexagon_image.get_height()))

    hexagon_image = pygame.transform.scale(hexagon_image, (height * .15, height * .15))
    window.blit(hexagon_image, (width / 4 * 2.5, height - hexagon_image.get_height() * 2))

    font_path = "./resources/fonts/Tektur-ExtraBold.ttf"
    font_size = int(height * 0.12)
    font_title = pygame.font.Font(font_path, font_size)
    font_start = pygame.font.Font(font_path, int(font_size / 3))

    text_hexagon = font_title.render("Hexagon", True, (255, 255, 255))
    text_puzzle = font_title.render("Puzzle", True, (255, 255, 255))
    text_play = font_start.render("PLAY", True, (255, 255, 255))
    text_exit = font_start.render("EXIT", True, (255, 255, 255))
    txt_h_width = text_hexagon.get_width()
    txt_h_height = text_hexagon.get_height()
    txt_p_width = text_puzzle.get_width()
    txt_p_height = text_puzzle.get_height()
    txt_s_width = text_play.get_width()
    txt_s_height = text_play.get_height()
    txt_e_width = text_exit.get_width()
    txt_e_height = text_exit.get_height()

    max_width = max(txt_s_width, txt_e_width)
    draw_hexagon(window,
                 (width / 2 - max_width / 2,
                  height / 4 + txt_h_height / 2 + txt_p_height / 4 * 3 + height / 5 + txt_s_height / 2),
                 int(font_size / 3), max_width)
    draw_hexagon(window,
                 (width / 2 - max_width / 2,
                  height / 4 + txt_h_height / 2 + txt_p_height / 4 * 3 + height / 5 + txt_e_height / 2 + txt_s_height / 2 + txt_s_height),
                 int(font_size / 3), max_width)
    window.blit(text_hexagon, (width / 2 - txt_h_width / 2, height / 4))
    window.blit(text_puzzle, (width / 2 - txt_p_width / 2, height / 4 + txt_h_height / 4 * 3))
    window.blit(text_play,
                (width / 2 - txt_s_width / 2, height / 4 + txt_h_height / 2 + txt_p_height / 4 * 3 + height / 5))
    window.blit(text_exit,
                (width / 2 - txt_e_width / 2,
                 height / 4 + txt_h_height / 4 * 3 + txt_p_height / 2 + height / 5 + txt_s_height / 2 + txt_s_height))

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if mouse_buttons[0] == 1:
        if width / 2 - txt_s_width / 2 < mouse_pos[
            0] < width / 2 + txt_s_width / 2 and height / 4 + txt_h_height / 2 + txt_p_height / 4 * 3 + height / 5 - txt_s_height / 2 < \
                mouse_pos[1] < height / 4 + txt_h_height / 4 * 3 + txt_p_height / 2 + height / 5 + txt_s_height:
            screen_data.set_screen_index(1)
        elif width / 2 - txt_s_width / 2 < mouse_pos[
            0] < width / 2 + txt_s_width / 2 and height / 4 + txt_h_height / 2 + txt_p_height / 4 * 3 + height / 5 - txt_s_height / 2+ txt_s_height / 2 + txt_s_height < \
                mouse_pos[1] < height / 4 + txt_h_height / 4 * 3 + txt_p_height / 2 + height / 5 + txt_s_height+ txt_s_height / 2 + txt_s_height:
            pygame.quit()
            sys.exit()


def draw_hexagon(screen, center, size, horizontal_line_length):
    points = []
    for i in range(6):
        angle_rad = math.radians(60 * i)
        x = int(center[0] + size * math.cos(angle_rad))
        y = int(center[1] + size * math.sin(angle_rad))
        points.append((x, y))

    points[0] = (points[0][0] + horizontal_line_length, points[0][1])
    points[1] = (points[1][0] + horizontal_line_length, points[1][1])
    points[5] = (points[5][0] + horizontal_line_length, points[5][1])

    pygame.draw.polygon(screen, (50, 50, 120), points)
    pygame.draw.lines(screen, (255, 255, 255), True, points, 3)
