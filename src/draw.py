import math

import pygame

from math_utils import sin60


def draw_hexagon_outline(window, x, y, side_length):
    points = []
    for i in range(6):
        angle = math.radians(60 * i + 90)
        x_point = x + side_length * math.cos(angle)
        y_point = y + side_length * math.sin(angle)
        points.append((x_point, y_point))
    pygame.draw.polygon(window, (60, 60, 82), points, 2)


def draw_hexagon(window: pygame.Surface, x: int, y: int, side_length: int, image) -> None:
    window.blit(image, (x - side_length, y - side_length))


def draw_hexagon_puzzle(window, x, y, side_length, color):
    points = []
    for i in range(6):
        angle = math.radians(60 * i + 90)
        x_point = x + side_length * math.cos(angle)
        y_point = y + side_length * math.sin(angle)
        points.append((x_point, y_point))
    pygame.draw.polygon(window, color, points)


def draw_tile(window, tile, side_length, coordinates, min_xy, images, image_map):
    for xx, yy in tile:
        x = coordinates[0] + (2 * (xx - min_xy[0]) + yy % 2) * side_length * sin60
        y = coordinates[1] + (yy - min_xy[1]) * side_length * 1.5
        window.blit(images[image_map[xx][yy]], (x - side_length, y - side_length))
        for i in range(6):
            n_x, n_y = map.get_neighbour_coordinates(xx, yy, i)
            b = False
            for t_x, t_y in tile:
                if n_x == t_x and n_y == t_y:
                    b = True
                    break
            if not b:
                angle1 = math.radians(60 * (i + 2) + 90)
                angle2 = math.radians(60 * (i + 3) + 90)
                x1 = x + side_length * math.cos(angle1)
                y1 = y + side_length * math.sin(angle1)
                x2 = x + side_length * math.cos(angle2)
                y2 = y + side_length * math.sin(angle2)
                pygame.draw.line(window, (255, 255, 255), (x1, y1), (x2, y2), 4)
