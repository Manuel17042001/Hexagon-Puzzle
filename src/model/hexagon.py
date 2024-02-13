from typing import Tuple


class Hexagon(object):

    def __init__(self, x: int, y: int, color: int) -> None:
        self.__x = x
        self.__y = y
        self.__color = color

    def get_x(self) -> int:
        return self.__x

    def set_x(self, x: int) -> None:
        self.__x = x

    def get_y(self) -> int:
        return self.__y

    def set_y(self, y: int):
        self.__y = y

    def get_coordinates(self) -> Tuple[int, int]:
        return self.__x, self.__y

    def get_color(self) -> int:
        return self.__color

    def __eq__(self, other: 'Hexagon') -> bool:
        return self.__x == other.get_x() and self.__y == other.get_y() and self.__color == other.get_color()
