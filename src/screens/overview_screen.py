import math
import sys

import pygame

from model.game_manager import GameManager
from model.screen_data import ScreenData
from utils import resource_holder, system_utils
from utils.draw_utils import draw_stretched_hexagon
from utils.math_utils import sin60

_buttons = []


def update() -> None:
    screen_data = ScreenData()
    window = screen_data.get_window()

    draw_background(window)

    font_path = "./resources/fonts/Tektur-ExtraBold.ttf"
    draw_title(window, font_path)

    draw_buttons(window, font_path)

    check_buttons()


def draw_background(window: pygame.Surface):
    width = window.get_width()
    height = window.get_height()

    background_image = resource_holder.image_background_start_screen
    background_image = pygame.transform.scale(background_image, (width, height))
    window.blit(background_image, (0, 0))

    hover_effect = math.sin(system_utils.time_in_millis() / 500) * 50

    hexagon_image = resource_holder.image_hexagon_start_screen
    hexagon_image = pygame.transform.scale(hexagon_image, (height * 0.7, height * .7))
    window.blit(hexagon_image, (width - hexagon_image.get_width() / 4 * 2.5,
                                -hexagon_image.get_height() * .1 + hover_effect))

    hexagon_image = pygame.transform.scale(hexagon_image, (height * .5, height * .5))
    hexagon_image2 = hexagon_image

    hexagon_image = pygame.transform.scale(hexagon_image, (height * .25, height * .25))
    window.blit(hexagon_image, (
        hexagon_image.get_width() * 0.8,
        hexagon_image.get_height() * 1.7 + hover_effect * .5 * .25))

    window.blit(hexagon_image2, (-hexagon_image.get_width() * .2,
                                 -hexagon_image.get_height() * .1 + hover_effect * .5))

    hexagon_image = pygame.transform.scale(hexagon_image, (height * .15, height * .15))
    window.blit(hexagon_image,
                (width / 4 * 2.5,
                 height - hexagon_image.get_height() * 2 + hover_effect * .5 * .25 * .15))


def draw_title(window: pygame.Surface, font_path: str):
    height = window.get_height()
    width = window.get_width()
    font_size = int(height * 0.12)
    font_title = pygame.font.Font(font_path, font_size)
    text_hexagon = font_title.render("Hexagon", True, (255, 255, 255))
    text_puzzle = font_title.render("Puzzle", True, (255, 255, 255))
    txt_h_w, txt_h_h = text_hexagon.get_size()
    txt_p_w, _ = text_puzzle.get_size()
    window.blit(text_hexagon, (width / 2 - txt_h_w / 2, height / 4))
    window.blit(text_puzzle, (width / 2 - txt_p_w / 2, height / 4 + txt_h_h / 4 * 3))


def draw_button(window, font_button, text, width, height, center):
    draw_stretched_hexagon(window, center, height, width, (0, 0, 0, 100), (255, 255, 255), 3)
    text_render = font_button.render(text, True, (255, 255, 255))
    window.blit(text_render, (center[0] - text_render.get_width() / 2, center[1] - text_render.get_height() / 2))


def draw_buttons(window: pygame.Surface, font_path: str):
    global _buttons
    exist_game = GameManager().exists_saved_game()

    text_button_1 = "Play"
    text_button_2 = "New Game"
    text_button_3 = "Exit"

    font_button = pygame.font.Font(font_path, int(window.get_height() * 0.04))
    width, height = font_button.render(text_button_2, True, (255, 255, 255)).get_size()

    height *= 0.75
    button_center = window.get_width() / 2, window.get_height() * 3 / 4

    _buttons = []

    if exist_game:
        draw_button(window, font_button, text_button_1, width, height,
                    (button_center[0], button_center[1] - height * 2))
        draw_button(window, font_button, text_button_2, width, height,
                    (button_center[0], button_center[1]))
        draw_button(window, font_button, text_button_3, width, height,
                    (button_center[0], button_center[1] + height * 2))

        _buttons.append(((button_center[0] - width / 2 - height, button_center[1] - height * 2 - height * sin60),
                         (button_center[0] + width / 2 + height, button_center[1] - height * 2 + height * sin60),
                         start_game))
        _buttons.append(((button_center[0] - width / 2 - height, button_center[1] - height * sin60),
                         (button_center[0] + width / 2 + height, button_center[1] + height * sin60),
                         start_new_game))
        _buttons.append(((button_center[0] - width / 2 - height, button_center[1] + height * 2 - height * sin60),
                         (button_center[0] + width / 2 + height, button_center[1] + height * 2 + height * sin60),
                         exit_game))
    else:
        draw_button(window, font_button, text_button_2, width, height,
                    (button_center[0], button_center[1] - height))
        draw_button(window, font_button, text_button_3, width, height,
                    (button_center[0], button_center[1] + height))

        _buttons.append(((button_center[0] - width / 2 - height, button_center[1] - height - height * sin60),
                         (button_center[0] + width / 2 + height, button_center[1] - height + height * sin60),
                         start_new_game))
        _buttons.append(((button_center[0] - width / 2 - height, button_center[1] + height - height * sin60),
                         (button_center[0] + width / 2 + height, button_center[1] + height + height * sin60),
                         exit_game))


def check_buttons():
    global _buttons
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0] == 1:
        for button in _buttons:
            begin, end, func = button
            if begin[0] < mouse_pos[0] < end[0] and begin[1] < mouse_pos[1] < end[1]:
                func()
                break


def start_game():
    GameManager().load_game()
    resource_holder.update_screen_data(ScreenData(), GameManager().get_game().get_map().get_grid_size())
    ScreenData().set_screen_index(1)


def start_new_game():
    GameManager().create_new_game(5, 4)
    ScreenData().set_screen_index(1)


def exit_game():
    pygame.quit()
    sys.exit()
