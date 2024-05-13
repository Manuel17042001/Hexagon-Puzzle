import copy
import math
import queue
import threading
import time

import pygame

from model import hexagonal_map
from model.game import Game
from model.game_manager import GameManager
from model.screen_data import ScreenData
from model.tile import Tile
from utils import draw_utils, resource_holder, system_utils
from utils.draw_utils import draw_stretched_hexagon, draw_rectangular_background, draw_hexagon_image
from utils.math_utils import sin60

pickup_mouse_pos: (float, float)
pickup_tile_pos: (float, float)
is_picked_up = False
picked_tile: Tile
start_grid_x, start_grid_y = 0, 0
mouse_pressed: bool = False

hexagons_hint: list[(int, int)] = []
colored_hint = False
last_no_solution_time = None
game = GameManager().get_game()
solved = False
loading_flag = False


def update() -> None:
    """
    This function is used to update the play screen based on the user input
    :param screen_data: the screen on witch it should be updated
    """
    global game, solved
    game = GameManager().get_game()

    screen_data = ScreenData()

    draw_layout(screen_data)

    draw_tiles(screen_data)

    draw_hint(screen_data)

    if solved:
        game.time_stop()
        draw_solved_overlay(screen_data)
        return
    elif game.get_map().is_puzzle_correctly():
        solved = True

    global last_no_solution_time
    if last_no_solution_time is not None and last_no_solution_time + 1000 > system_utils.time_in_millis():
        font_path = "./resources/fonts/Tektur-ExtraBold.ttf"
        font_size = int(screen_data.get_window().get_height() * 0.1)
        font = pygame.font.Font(font_path, int(font_size / 3))
        text_no_solution = font.render("No solution found!", True, (255, 0, 0))
        window = screen_data.get_window()
        width, height = window.get_size()
        txt_width, txt_height = text_no_solution.get_size()
        draw_stretched_hexagon(window, (
            width / 4 - txt_width / 2 + text_no_solution.get_width() / 2, height / 4 * 2.5 + txt_height / 2),
                               int(font_size / 3), txt_width, (255, 255, 255, 150), (255, 255, 255), 3)
        window.blit(text_no_solution, (width / 4 - txt_width / 2, height / 4 * 2.5))

    if not solved:
        game.time_run()
        update_mouse_movement(screen_data)


def draw_solved_overlay(screen_data: ScreenData) -> None:
    window = screen_data.get_window()
    width, height = window.get_size()
    draw_rectangular_background(window, (width / 2, height / 2), width, height,
                                (0, 0, 0, 150),
                                (0, 0, 0), 1)
    draw_rectangular_background(window, (width / 2, height / 2), width / 5 * 3, height / 5 * 3,
                                (20, 20, 31, 200),
                                (255, 255, 255), 3)

    font_size = int(height * 0.12)
    font_path = "./resources/fonts/Tektur-ExtraBold.ttf"
    font_title = pygame.font.Font(font_path, font_size)
    font_subtitle = pygame.font.Font(font_path, int(font_size * 0.45))
    text_hexagon_puzzle = font_subtitle.render("Hexagon Puzzle", True, (255, 255, 255))
    text_solved = font_title.render("Solved!", True, (255, 255, 255))
    txt_hp_w, txt_hp_h = text_hexagon_puzzle.get_size()
    window.blit(text_hexagon_puzzle, (width / 2 - txt_hp_w / 2, height / 4))
    txt_s_w, txt_s_h = text_solved.get_size()
    window.blit(text_solved, (width / 2 - txt_s_w / 2, height / 4 + txt_hp_h / 2))
    font_button = pygame.font.Font(font_path, int(font_size * 0.4))
    text_no_solution = font_button.render("Home", True, (255, 255, 255))
    window = screen_data.get_window()
    width, height = window.get_size()
    txt_width, txt_height = text_no_solution.get_size()
    draw_stretched_hexagon(window, (width / 2, height * 3 / 5),
                           int(font_size / 3), txt_width, (255, 255, 255, 150), (255, 255, 255), 3)
    window.blit(text_no_solution, (width / 2 - txt_width / 2, height * 3 / 5 - txt_height / 2))

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if mouse_buttons[0] == 1:
        if (width / 2 - txt_width / 2 < mouse_pos[0] < width / 2 + txt_width / 2 and
                height * 3 / 5 - txt_height / 2 < mouse_pos[1] < height * 3 / 5 + txt_height / 2):
            GameManager().delete_saved_game()
            global hexagons_hint, solved
            solved = False
            hexagons_hint = []
            screen_data.set_screen_index(0)


def draw_layout(screen_data: ScreenData) -> None:
    window = ScreenData().get_window()
    grid_width, grid_height = GameManager().get_game().get_map().get_grid_size()
    window_width, window_height = window.get_width(), window.get_height()

    window.fill(screen_data.get_background_color())

    side_length = screen_data.get_hexagon_side_length()
    global start_grid_x, start_grid_y

    n_x = int((window_width / 2) / 2 / sin60 / side_length - 1 / 2 + 2)
    n_y = int(((window_height / 4 * 3) / side_length - 1 / 2) * 2 / 3 + 2)

    grid_x_start = int((n_x - grid_width) / 2) - 1
    grid_y_start = int((n_y - grid_height) / 2)

    if not grid_y_start % 2:
        grid_y_start -= 1

    start_grid_x = (2 * (grid_x_start - 1) + (grid_y_start - 1) % 2) * side_length * sin60
    start_grid_y = (grid_y_start - 1) * side_length * 1.5

    if not game.is_play_ground_initialised():
        for tile in game.get_map().get_tiles():
            if not tile.is_moveable():
                tile.set_pos_x(start_grid_x)
                tile.set_pos_y(start_grid_y)
        game.set_play_ground_initialised()

    window.blit(resource_holder.grid_image, (0, 0))

    pygame.draw.rect(window, (20, 20, 31), ((window_width / 2, 0), (window_width, window_height)))
    pygame.draw.rect(window, (20, 20, 31), ((0, window_height * 3 / 4), (window_width / 2, window_height)))
    pygame.draw.rect(window, (50, 50, 70), ((window_width / 2, 0), (window_width / 2, window_height / 15)))
    pygame.draw.rect(window, (0, 0, 0),
                     ((window_width / 2, window_height / 15), (window_width / 2, window_height / 15 * 0.05)))

    game_time = int(game.get_time())
    seconds = game_time % 60
    minute = game_time // 60
    font_path = "./resources/fonts/Tektur-ExtraBold.ttf"
    font_size = int(window_height * 0.12)
    font_time = pygame.font.Font(font_path, int(font_size * 0.2))
    text_time = font_time.render(f" Time {str(minute).zfill(2)}:{str(seconds).zfill(2)}", True, (255, 255, 255))
    txt_width, txt_height = text_time.get_size()
    window.blit(text_time, (window_width / 2 + (window_height / 15 / 2 - txt_height / 2),
                            window_height / 15 / 2 - txt_height / 2))

    window.blit(resource_holder.image_icon_exit, (window_width - resource_holder.image_icon_exit.get_width(), 0))
    window.blit(resource_holder.image_icon_hint, (
        window_width - resource_holder.image_icon_exit.get_width() - resource_holder.image_icon_hint.get_width(), 0))
    window.blit(resource_holder.image_icon_colored_hint, (
        window_width - resource_holder.image_icon_exit.get_width() - resource_holder.image_icon_hint.get_width() - resource_holder.image_icon_colored_hint.get_width(),
        0))

    colored_hint_count, hint_count = game.get_colored_hint_count(), game.get_hint_count()
    font_time = pygame.font.Font(font_path, int(font_size * 0.13))
    text_colored_hint_count = font_time.render(f"{colored_hint_count}", True, (150, 150, 150))
    txt_width, txt_height = text_colored_hint_count.get_size()
    window.blit(text_colored_hint_count, (
        window_width - resource_holder.image_icon_exit.get_width() - resource_holder.image_icon_hint.get_width() - txt_width,
        window_height / 15 - txt_height))
    text_hint_count = font_time.render(f"{hint_count}", True, (150, 150, 150))
    txt_width, txt_height = text_hint_count.get_size()
    window.blit(text_hint_count, (
        window_width - resource_holder.image_icon_exit.get_width() - txt_width,
        window_height / 15 - txt_height))

    image_size = resource_holder.image_flip_vertical.get_size()

    image_offset_x = (window_width / 4 - image_size[0]) / 2
    image_offset_y = (window_height / 4 - image_size[1]) / 2

    window.blit(resource_holder.image_flip_vertical,
                (window_width / 4 * 0 + image_offset_x, window_height * 3 / 4 + image_offset_y))
    window.blit(resource_holder.image_flip_horizontal,
                (window_width / 4 * 1 + image_offset_x, window_height * 3 / 4 + image_offset_y))
    window.blit(resource_holder.image_rotation_right,
                (window_width / 4 * 2 + image_offset_x, window_height * 3 / 4 + image_offset_y))
    window.blit(resource_holder.image_rotation_left,
                (window_width / 4 * 3 + image_offset_x, window_height * 3 / 4 + image_offset_y))

    pygame.draw.line(window,
                     (255, 255, 255),
                     (0, window_height * 3 / 4),
                     (window_width, window_height * 3 / 4),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 4, window_height * 3 / 4),
                     (window_width / 4, window_height),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 4 * 2, window_height * 3 / 4),
                     (window_width / 4 * 2, window_height),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 4 * 3, window_height * 3 / 4),
                     (window_width / 4 * 3, window_height),
                     3)

    pygame.draw.line(window,
                     (255, 255, 255),
                     (window_width / 2, 0),
                     (window_width / 2, window_height),
                     3)


def remove_tile_from_actual_map(tile: Tile) -> None:
    previous_grid_pos = tile.get_grid_pos()
    if tile.get_grid_pos() is not None:
        grid_pos_x, grid_pos_y = previous_grid_pos
        actual_map = game.get_map().get_actual_map()

        for hexagon in tile.get_hexagons():
            hexagon_grid_y = hexagon.get_y() + grid_pos_y
            hexagon_grid_x = hexagon.get_x() + grid_pos_x + (grid_pos_y % 2 != 0 and hexagon_grid_y % 2 == 0)
            actual_map[hexagon_grid_y][hexagon_grid_x] = None

        tile.set_grid_pos(None)


def add_tile_to_actual_map(tile: Tile) -> None:
    grid_width, grid_height = game.get_map().get_grid_size()
    grid_pos_x, grid_pos_y = tile.get_grid_pos()
    actual_map = copy.deepcopy(game.get_map().get_actual_map())

    for hexagon in tile.get_hexagons():
        hexagon_grid_y = hexagon.get_y() + grid_pos_y
        hexagon_grid_x = hexagon.get_x() + grid_pos_x + (grid_pos_y % 2 != 0 and hexagon_grid_y % 2 == 0)

        if 0 < hexagon_grid_x <= grid_width and 0 < hexagon_grid_y <= grid_height and \
                actual_map[hexagon_grid_y][hexagon_grid_x] is None:
            actual_map[hexagon_grid_y][hexagon_grid_x] = hexagon.get_color()
        else:
            tile.set_pos_x(pickup_tile_pos[0])
            tile.set_pos_y(pickup_tile_pos[1])
            tile.set_grid_pos(None)
            break

    if tile.get_grid_pos() is not None:
        game.get_map().set_actual_map(actual_map)


def pickup_tile(screen_data: ScreenData, mouse_pos: (int, int)) -> None:
    global picked_tile
    global pickup_tile_pos
    global pickup_mouse_pos
    global is_picked_up

    mouse_x, mouse_y = mouse_pos
    tiles = game.get_map().get_tiles()
    side_length = screen_data.get_hexagon_side_length()

    for tile in tiles:
        if not tile.is_moveable():
            continue
        tile_pos = tile.get_position()
        for hexagon in tile.get_hexagons():
            grid_x, grid_y = hexagon.get_coordinates()
            grid_x = tile.get_pos_x() + (2 * grid_x + grid_y % 2) * side_length * sin60
            grid_y = tile.get_pos_y() + grid_y * side_length * 1.5
            distance = math.sqrt((grid_x - mouse_x) ** 2 + (grid_y - mouse_y) ** 2)
            if distance < side_length:
                pickup_mouse_pos = mouse_pos
                pickup_tile_pos = copy.copy(tile_pos)
                picked_tile = tile
                is_picked_up = True

                # move tile to the end
                tile_tmp = picked_tile
                tiles.remove(tile_tmp)
                tiles.append(tile_tmp)

                # remove from actual map
                remove_tile_from_actual_map(picked_tile)
                break


def check_is_pos_in_grid(position: (float, float), screen_data: ScreenData) -> ((float, float), (int, int)):
    pos_y, pos_x = position
    side_length = screen_data.get_hexagon_side_length()
    grid_width, grid_height = game.get_map().get_grid_size()

    for grid_y in range(1, grid_height + 1):
        for grid_x in range(1, grid_width + 1):
            pos_grid_x = start_grid_x + (2 * grid_x + grid_y % 2) * side_length * sin60
            pos_grid_y = start_grid_y + grid_y * side_length * 1.5
            distance = math.sqrt((pos_grid_x - pos_y) ** 2 + (pos_grid_y - pos_x) ** 2)
            if distance < side_length:
                return (pos_grid_x, pos_grid_y), (grid_x, grid_y)
    return None, None


def update_tile_shape(grid_x, screen_data: ScreenData) -> None:
    window = screen_data.get_window()
    window_width = window.get_width()
    if grid_x < screen_data.get_window().get_width() / 4:
        picked_tile.flip_horizontal()
    elif grid_x < screen_data.get_window().get_width() / 2:
        picked_tile.flip_vertical()
    else:
        picked_tile.rotate(grid_x > window_width / 4 * 3)


def put_down_tile(screen_data: ScreenData) -> None:
    global is_picked_up
    global pickup_tile_pos

    side_length = screen_data.get_hexagon_side_length()
    is_picked_up = False

    window = screen_data.get_window()
    window_width, window_height = window.get_width(), window.get_height()

    # check if tile is in grid
    pos_tile = picked_tile.get_pos_x(), picked_tile.get_pos_y()
    pos_grid_xy, grid_xy = check_is_pos_in_grid(pos_tile, screen_data)
    if grid_xy is not None:
        picked_tile.set_pos_x(pos_grid_xy[0])
        picked_tile.set_pos_y(pos_grid_xy[1])
        picked_tile.set_grid_pos((grid_xy[0], grid_xy[1]))
        # add tile to actual_map
        add_tile_to_actual_map(picked_tile)
    else:
        for hexagon in picked_tile.get_hexagons():
            grid_x, grid_y = hexagon.get_coordinates()
            grid_x = picked_tile.get_pos_x() + (2 * grid_x + grid_y % 2) * side_length * sin60
            grid_y = picked_tile.get_pos_y() + grid_y * side_length * 1.5
            if ((grid_x < screen_data.get_window().get_width() / 2 + side_length or
                 grid_x > window_width - side_length or
                 grid_y < side_length or
                 grid_y > window_height - side_length) or
                    grid_y > window_height * 3 / 4):
                if grid_y > window_height * 3 / 4:
                    update_tile_shape(grid_x, screen_data)
                    if pickup_tile_pos[0] < window_width / 2:
                        pickup_tile_pos = [window_width / 4 * 3, window_height / 4 * 3 / 2]
                picked_tile.set_pos_x(pickup_tile_pos[0])
                picked_tile.set_pos_y(pickup_tile_pos[1])
        pos_tile = picked_tile.get_position()
        pos_grid_xy, grid_xy = check_is_pos_in_grid(pos_tile, screen_data)
        if grid_xy is not None:
            picked_tile.set_grid_pos((grid_xy[0], grid_xy[1]))
            add_tile_to_actual_map(picked_tile)


def update_picked_tile_pos(mouse_pos) -> None:
    global picked_tile
    picked_tile.set_pos_x(mouse_pos[0] - pickup_mouse_pos[0] + pickup_tile_pos[0])
    picked_tile.set_pos_y(mouse_pos[1] - pickup_mouse_pos[1] + pickup_tile_pos[1])


def update_mouse_movement(screen_data):
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    window = screen_data.get_window()
    window_width, window_height = window.get_width(), window.get_height()

    global is_picked_up
    global mouse_pressed
    global hexagons_hint
    global colored_hint
    global last_no_solution_time

    if mouse_buttons[0] == 1:
        mouse_pressed = True

    if mouse_buttons[0] == 0 and mouse_pressed is True:
        mouse_pressed = False
        if mouse_pos[0] > window_width - resource_holder.image_icon_exit.get_width() and mouse_pos[
            1] < window_height / 15:
            hexagons_hint = []
            game.time_stop()
            GameManager().save_game()
            screen_data.set_screen_index(0)
        elif mouse_pos[0] > window_width - resource_holder.image_icon_exit.get_width() * 3 and mouse_pos[
            1] < window_height / 15:
            colored_hint = not mouse_pos[0] > window_width - resource_holder.image_icon_exit.get_width() * 2
            global loading_flag
            loading_flag = True
            result = queue.Queue()
            loading_thread = threading.Thread(target=show_loading_screen, args=(screen_data,))
            hint_thread = threading.Thread(target=get_hint, args=(game, result))
            game.time_stop()
            loading_thread.start()
            hint_thread.start()
            hint_thread.join()
            game.time_run()
            loading_flag = False
            hint = result.get()
            if hint is not None:
                hexagons_hint = game.get_hint(game)[1]
                if colored_hint is True:
                    game.increase_colored_hint_count()
                else:
                    game.increase_hint_count()
            else:
                game.increase_hint_count()
                hexagons_hint = []
                last_no_solution_time = system_utils.time_in_millis()

    if mouse_buttons[0] == 1 and not is_picked_up:
        pickup_tile(screen_data, mouse_pos)

    elif mouse_buttons[0] == 0 and is_picked_up:
        put_down_tile(screen_data)

    if is_picked_up:
        update_picked_tile_pos(mouse_pos)


def show_loading_screen(screen_data):
    global loading_flag
    n_dots = 0
    time.sleep(0.5)
    while loading_flag:
        window = screen_data.get_window()
        width, height = window.get_size()

        l_width, l_height = width / 6 * 2, height / 7

        rect = pygame.Rect(width / 2 - l_width / 2, height / 2 - l_height / 2, l_width, l_height)
        draw_rectangular_background(window, (width / 2, height / 2), rect.width, rect.height,
                                    (20, 20, 31, 255),
                                    (255, 255, 255), 3)

        max_dots = 3
        text = "Searching for solution"

        font_size = int(height * 0.036)
        font_path = "./resources/fonts/Tektur-ExtraBold.ttf"
        font_title = pygame.font.Font(font_path, font_size)
        text_ref = font_title.render(text + "." * max_dots, True, (255, 255, 255))
        for _ in range(n_dots % (max_dots + 1)):
            text += "."
        n_dots += 1
        text_load = font_title.render(text, True, (255, 255, 255))
        txt_s_w, txt_s_h = text_ref.get_size()
        window.blit(text_load, (width / 2 - txt_s_w / 2, height / 2 - txt_s_h / 2))
        pygame.display.update(rect)
        time.sleep(0.5)


def get_hint(game: Game, result):
    hint = game.get_hint(game)
    result.put(hint)


def draw_tiles(screen_data):
    image_o = resource_holder.image_hexagon_orange
    image_b = resource_holder.image_hexagon_blue
    sl = screen_data.get_hexagon_side_length()
    for tile in game.get_map().get_tiles():
        t_x, t_y = tile.get_position()
        for hexagon in tile.get_hexagons():
            image = image_b if hexagon.get_color() == 0 else image_o
            h_x, h_y = hexagon.get_coordinates()
            draw_utils.draw_hexagon_image(screen_data.get_window(),
                                          (t_x + (2 * h_x + h_y % 2) * sl * sin60,
                                           t_y + h_y * sl * 1.5),
                                          screen_data.get_hexagon_side_length(),
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
                    if tile.is_moveable():
                        pygame.draw.line(screen_data.get_window(), (255, 255, 255), (x1, y1), (x2, y2), 5)


def draw_hint(screen_data):
    window = screen_data.get_window()
    window_width, window_height = window.get_width(), window.get_height()
    grid_width, grid_height = game.get_map().get_grid_size()
    sl = screen_data.get_hexagon_side_length()
    n_x = int((window_width / 2) / 2 / sin60 / sl - 1 / 2 + 2)
    n_y = int(((window_height / 4 * 3) / sl - 1 / 2) * 2 / 3 + 2)

    grid_x_start = int((n_x - grid_width) / 2) - 1 - 1
    grid_y_start = int((n_y - grid_height) / 2) - 2 + 1 - int((grid_height + 1) / 2) % 2
    t_x = (2 * grid_x_start + grid_y_start % 2) * sl * sin60
    t_y = grid_y_start * sl * 1.5
    global hexagons_hint
    global colored_hint
    for hexagon in hexagons_hint:
        coord, color = hexagon
        h_x, h_y = coord
        if colored_hint:
            x = t_x + (2 * h_x + h_y % 2) * sl * sin60
            y = t_y + h_y * sl * 1.5
            image = copy.copy(
                resource_holder.image_hexagon_orange if color == 1 else resource_holder.image_hexagon_blue)
            image.set_alpha(100)
            draw_hexagon_image(window, (x, y), sl, image)
        for i in range(6):
            n_x, n_y = hexagonal_map.get_neighbour_coordinates(h_x, h_y, i)
            b = False
            for hexagon1 in hexagons_hint:
                coord1, _ = hexagon1
                xx, yy = coord1
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
                pygame.draw.line(screen_data.get_window(), (103, 255, 0), (x1, y1), (x2, y2), 3)
