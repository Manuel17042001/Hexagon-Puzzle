from copy import deepcopy

import math_utils
from model.hexagon import Hexagon


class Tile(object):

    def __init__(self, pos_x: float, pos_y: float, hexagons: list[Hexagon]):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__hexagons = hexagons

    def get_pos_x(self) -> float:
        return self.__pos_x

    def set_pos_x(self, pos_x: float) -> None:
        self.__pos_x = pos_x

    def get_pos_y(self) -> float:
        return self.__pos_y

    def get_position(self) -> tuple[float, float]:
        return self.__pos_x, self.__pos_y

    def set_pos_y(self, pos_y: float) -> None:
        self.__pos_y = pos_y

    def get_hexagons(self) -> list[Hexagon]:
        return self.__hexagons

    def normalise_hexagon_pos(self):
        hexagons = deepcopy(self.__hexagons)
        hexagon_0_x, hexagon_0_y = hexagons[0].get_coordinates()

        if hexagon_0_x == 0 and hexagon_0_y == 0:
            return hexagons

        y_dif = -hexagon_0_y
        x_dif = -hexagon_0_x

        if hexagon_0_y % 2 == 0:
            for hexagon in hexagons:
                hexagon.set_x(hexagon.get_x() + x_dif)
                hexagon.set_y(hexagon.get_y() + y_dif)
        else:
            for hexagon in hexagons:
                new_y = hexagon.get_y() + y_dif
                hexagon.set_y(new_y)
                hexagon.set_x(hexagon.get_x() + x_dif - new_y % 2)

        self.__hexagons = hexagons

    def flip(self):
        for hexagon in self.__hexagons:
            hexagon.set_y(-hexagon.get_y())

    def rotate(self, direction: bool):
        # todo: info -> https://gamedev.stackexchange.com/questions/15237/how-do-i-rotate-a-structure-of-hexagonal-tiles-on-a-hexagonal-grid
        for hexagon in self.__hexagons:
            x, y = hexagon.get_coordinates()

            x, y = math_utils.oddr_to_axial(x, y)

            q, r, s = math_utils.axial_to_cube(x, y)

            if direction:
                q, r, s = -s, -q, -r
            else:
                q, r, s = -r, -s, -q

            x, y = math_utils.cube_to_axial(q, r, s)

            x, y = math_utils.axial_to_oddr(x, y)

            hexagon.set_x(x)
            hexagon.set_y(y)
