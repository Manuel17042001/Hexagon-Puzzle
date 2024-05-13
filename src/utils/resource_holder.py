import pygame

import utils.draw_utils as draw_utils
from utils.math_utils import sin60

__side_length = 10

image_background_start_screen = pygame.image.load("./resources/background/1000x1500.png")
image_hexagon_start_screen = pygame.image.load("./resources/hexagon_splash_screen.png")
image_icon = pygame.image.load("./resources/icon.png")

image_hexagon_orange_unscaled = pygame.image.load("./resources/hexagon_orange.png")
image_hexagon_blue_unscaled = pygame.image.load("./resources/hexagon_blue.png")
image_hexagon_orange = pygame.transform.smoothscale(image_hexagon_orange_unscaled, (2 * __side_length, 2 * __side_length))
image_hexagon_blue = pygame.transform.smoothscale(image_hexagon_blue_unscaled, (2 * __side_length, 2 * __side_length))

image_rotation_left_unscaled = pygame.image.load("./resources/rotation_left.png")
image_rotation_right_unscaled = pygame.image.load("./resources/rotation_right.png")
image_rotation_left = image_rotation_left_unscaled
image_rotation_right = image_rotation_right_unscaled

image_flip_vertical_unscaled = pygame.image.load("./resources/flip_vertical.png")
image_flip_horizontal_unscaled = pygame.image.load("./resources/flip_horizontal.png")
image_flip_vertical = image_flip_vertical_unscaled
image_flip_horizontal = image_flip_horizontal_unscaled

image_icon_exit_unscaled = pygame.image.load("./resources/exit_icon.png")
image_icon_exit = image_icon_exit_unscaled

image_icon_hint_unscaled = pygame.image.load("./resources/hint_icon.png")
image_icon_hint = image_icon_hint_unscaled
image_icon_colored_hint_unscaled = pygame.image.load("./resources/colored_hint_icon.png")
image_icon_colored_hint = image_icon_colored_hint_unscaled

grid_image = pygame.Surface((0, 0), pygame.SRCALPHA)


def update_screen_data(screen, grid_size):
    global __side_length
    global image_hexagon_blue
    global image_hexagon_orange
    global image_rotation_left
    global image_rotation_right
    global image_flip_horizontal
    global image_flip_vertical
    global image_icon_exit
    global image_icon_hint
    global image_icon_colored_hint

    window = screen.get_window()

    __side_length = screen.get_hexagon_side_length()
    image_hexagon_orange = pygame.transform.scale(image_hexagon_orange_unscaled, (2 * __side_length, 2 * __side_length))
    image_hexagon_blue = pygame.transform.scale(image_hexagon_blue_unscaled, (2 * __side_length, 2 * __side_length))

    scale = min(window.get_width(), window.get_height()) / 6
    scale_rotation_flip_image = (scale, scale)
    image_rotation_left = pygame.transform.smoothscale(image_rotation_left_unscaled, scale_rotation_flip_image)
    image_rotation_right = pygame.transform.smoothscale(image_rotation_right_unscaled, scale_rotation_flip_image)
    image_flip_vertical = pygame.transform.smoothscale(image_flip_vertical_unscaled, scale_rotation_flip_image)
    image_flip_horizontal = pygame.transform.smoothscale(image_flip_horizontal_unscaled, scale_rotation_flip_image)

    icon_scale = window.get_height() / 15
    image_icon_exit = pygame.transform.smoothscale(image_icon_exit_unscaled, (icon_scale, icon_scale))
    image_icon_hint = pygame.transform.smoothscale(image_icon_hint_unscaled, (icon_scale, icon_scale))
    image_icon_colored_hint = pygame.transform.smoothscale(image_icon_colored_hint_unscaled, (icon_scale, icon_scale))

    __update_grid_image(screen, grid_size)


def __update_grid_image(screen, grid_size):
    global grid_image
    window = screen.get_window()
    grid_width, grid_height = grid_size
    window_width, window_height = window.get_width(), window.get_height()
    grid_image = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    n_x = int((window_width / 2) / 2 / sin60 / __side_length - 1 / 2 + 2)
    n_y = int(((window_height / 4 * 3) / __side_length - 1 / 2) * 2 / 3 + 2)

    grid_x_start = int((n_x - grid_width) / 2) - 1
    grid_y_start = int((n_y - grid_height) / 2)

    if not grid_y_start % 2:
        grid_y_start -= 1

    for y in range(n_y):
        for x in range(n_x):
            if grid_x_start <= x < grid_x_start + grid_width and grid_y_start <= y < grid_y_start + grid_height:
                draw_utils.draw_hexagon_outline(grid_image,
                                                ((2 * x + y % 2) * __side_length * sin60, y * __side_length * 1.5),
                                                __side_length, (60, 60, 82), 2)
            else:
                draw_utils.draw_hexagon_image(grid_image,
                                              ((2 * x + y % 2) * __side_length * sin60,
                                               int(y * __side_length * 1.5)),
                                              __side_length,
                                              image_hexagon_blue)
