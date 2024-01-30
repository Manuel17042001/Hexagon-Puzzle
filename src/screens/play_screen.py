import copy
import math

import pygame

import draw
import hexagonal_map
import resource_holder
from math_utils import sin60
from model.game import Game
from screens.screen_data import ScreenData

mouse_xy = 0, 0
tile_xy = 0, 0
is_picked_up = False
picked_item = None
start_grid_x, start_grid_y = 0, 0


def update(screen_data: ScreenData, game: Game) -> None:
    """
    This function is used to update the play screen based on the user input
    :param screen_data: the screen on witch it should be updated
    :param game: the game with the infos about the tiles and grid
    """
    draw_layout(screen_data, game)

    update_mouse_movement(screen_data, game)

    draw_tiles(screen_data, game)


def draw_layout(screen_data: ScreenData, game: Game) -> None:
    window = screen_data.get_window()
    grid_width, grid_height = game.get_map().get_grid_size()
    window_width, window_height = window.get_width(), window.get_height()

    window.fill(screen_data.get_background_color())

    side_length = screen_data.get_side_length()
    global start_grid_x, start_grid_y

    n_x = int((window_width / 2) / 2 / sin60 / side_length - 1 / 2 + 2)
    n_y = int(((window_height / 4 * 3) / side_length - 1 / 2) * 2 / 3 + 2)

    grid_x_start = int((n_x - grid_width) / 2) - 1
    grid_y_start = int((n_y - grid_height) / 2)

    if not grid_y_start % 2:
        grid_y_start -= 1

    start_grid_x = (2 * (grid_x_start - 1) + (grid_y_start - 1) % 2) * side_length * sin60
    start_grid_y = (grid_y_start - 1) * side_length * 1.5

    window.blit(resource_holder.grid_image, (0, 0))

    pygame.draw.rect(window, (20, 20, 31), ((window_width / 2, 0), (window_width, window_height)))
    pygame.draw.rect(window, (20, 20, 31), ((0, window_height * 3 / 4), (window_width / 2, window_height)))

    window.blit(resource_holder.image_rotation_right,
                (window_width / 2 / 3 * 1.25, window_height * 3 / 4 + window_width / 2 / 3 * 0.25))
    window.blit(resource_holder.image_rotation_left,
                (window_width / 2 / 3 * 2 + window_width / 2 / 3 * 0.25,
                 window_height * 3 / 4 + window_width / 2 / 3 * 0.25))
    window.blit(resource_holder.image_flip,
                (window_width / 2 / 3 * 0.25, window_height * 3 / 4 + window_width / 2 / 3 * 0.25))

    pygame.draw.line(window,
                     (255, 255, 255),
                     (0, window_height * 3 / 4),
                     (window_width / 2, window_height * 3 / 4),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 2 / 3, window_height * 3 / 4),
                     (window_width / 2 / 3, window_height),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 2 / 3 * 2, window_height * 3 / 4),
                     (window_width / 2 / 3 * 2, window_height),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 2, 0),
                     (window_width / 2, window_height),
                     3)


def update_mouse_movement(screen_data, game):
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    global mouse_xy
    global tile_xy
    global is_picked_up
    global picked_item
    tiles = game.get_map().get_tiles()
    side_length = screen_data.get_side_length()
    grid_width, grid_height = game.get_map().get_grid_size()
    global start_grid_x, start_grid_y

    if mouse_buttons[0] == 1 and not is_picked_up:
        for i in range(len(tiles)):
            tile = tiles[i]
            tile_pos = tile.get_position()
            for hexagon in tile.get_hexagons():
                grid_x, grid_y = hexagon.get_coordinates()
                grid_x = tile.get_pos_x() + (2 * grid_x + grid_y % 2) * side_length * sin60
                grid_y = tile.get_pos_y() + grid_y * side_length * 1.5
                distance = math.sqrt((grid_x - mouse_x) ** 2 + (grid_y - mouse_y) ** 2)
                if distance < side_length:
                    picked_item = i
                    mouse_xy = mouse_x, mouse_y
                    tile_xy = copy.copy(tile_pos)
                    is_picked_up = True
                    # move tile to the end
                    tile_tmp = tiles[picked_item]
                    tiles.remove(tile_tmp)
                    tiles.append(tile_tmp)
                    break

    elif mouse_buttons[0] == 0 and is_picked_up:
        is_picked_up = False
        picked_tile = tiles[picked_item]
        tile_in_grid = False

        t_x, t_y = picked_tile.get_position()
        for grid_y in range(1, grid_height + 1):
            for grid_x in range(1, grid_width + 1):
                pos_grid_x = start_grid_x + (2 * grid_x + grid_y % 2) * side_length * sin60
                pos_grid_y = start_grid_y + grid_y * side_length * 1.5
                distance = math.sqrt((pos_grid_x - t_x) ** 2 + (pos_grid_y - t_y) ** 2)
                if distance < side_length:
                    picked_tile.set_pos_x(pos_grid_x)
                    picked_tile.set_pos_y(pos_grid_y)
                    tile_in_grid = True
                    break

        # todo check if the tile is inside the puzzle and save the puzzle if it is inside->->
        window = screen_data.get_window()
        window_width, window_height = window.get_width(), window.get_height()

        if not tile_in_grid:
            for hexagon in picked_tile.get_hexagons():
                grid_x, grid_y = hexagon.get_coordinates()
                grid_x = picked_tile.get_pos_x() + (2 * grid_x + grid_y % 2) * side_length * sin60
                grid_y = picked_tile.get_pos_y() + grid_y * side_length * 1.5
                if grid_x < screen_data.get_window().get_width() / 2 + side_length or grid_x > window_width - side_length or grid_y < side_length or grid_y > window_height - side_length:
                    if grid_x < screen_data.get_window().get_width() / 2 / 3:
                        tiles[picked_item].flip()
                    else:
                        tiles[picked_item].rotate(grid_x > screen_data.get_window().get_width() / 2 / 3 * 2)
                    tiles[picked_item].set_pos_x(tile_xy[0])
                    tiles[picked_item].set_pos_y(tile_xy[1])

    if is_picked_up:
        tiles[picked_item].set_pos_x(mouse_x - mouse_xy[0] + tile_xy[0])
        tiles[picked_item].set_pos_y(mouse_y - mouse_xy[1] + tile_xy[1])


def draw_tiles(screen_data, game):
    image_o = resource_holder.image_hexagon_orange
    image_b = resource_holder.image_hexagon_blue
    sl = screen_data.get_side_length()
    for tile in game.get_map().get_tiles():
        t_x, t_y = tile.get_position()
        for hexagon in tile.get_hexagons():
            image = image_b if hexagon.get_color() == 0 else image_o
            h_x, h_y = hexagon.get_coordinates()
            draw.draw_hexagon(screen_data.get_window(),
                              t_x + (2 * h_x + h_y % 2) * sl * sin60,
                              t_y + h_y * sl * 1.5,
                              screen_data.get_side_length(),
                              image)
            for i in range(6):
                n_x, n_y = hexagonal_map.get_neighbour_coordinates(h_x, h_y, i)
                b = False
                for hexagon1 in tile.get_hexagons():
                    xx, yy = hexagon1.get_coordinates()
                    if n_x == xx and n_y == yy:
                        b = True
                        break
                if not b:
                    angle1 = math.radians(60 * (i + 2) + 90)
                    angle2 = math.radians(60 * (i + 3) + 90)
                    x1 = t_x + (2 * h_x + h_y % 2) * sl * sin60 + sl * math.cos(angle1)
                    y1 = t_y + h_y * sl * 1.5 + sl * math.sin(angle1)
                    x2 = t_x + (2 * h_x + h_y % 2) * sl * sin60 + sl * math.cos(angle2)
                    y2 = t_y + h_y * sl * 1.5 + sl * math.sin(angle2)
                    pygame.draw.line(screen_data.get_window(), (255, 255, 255), (x1, y1), (x2, y2), 5)
