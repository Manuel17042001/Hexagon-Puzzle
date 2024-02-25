from typing import Tuple


class Hexagon:
    def __init__(self, x: int, y: int, color: int) -> None:
        """
        Initialize a Hexagon object with coordinates and color.
        :param x: The x-coordinate of the hexagon.
        :param y: The y-coordinate of the hexagon.
        :param color: The color of the hexagon.
        """
        self.__x = x  # Initialize x-coordinate
        self.__y = y  # Initialize y-coordinate
        self.__color = color  # Initialize color

    def set_coordinates(self, x: int, y: int) -> None:
        """
        Set the coordinates of the hexagon.
        :param x: The new x-coordinate of the hexagon.
        :param y: The new y-coordinate of the hexagon.
        """
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        """Get the x-coordinate of the hexagon."""
        return self.__x

    def set_x(self, x: int) -> None:
        """Set the x-coordinate of the hexagon."""
        self.__x = x

    def get_y(self) -> int:
        """Get the y-coordinate of the hexagon."""
        return self.__y

    def set_y(self, y: int):
        """Set the y-coordinate of the hexagon."""
        self.__y = y

    def get_coordinates(self) -> Tuple[int, int]:
        """Get the coordinates of the hexagon as a tuple (x, y)."""
        return self.__x, self.__y

    def get_color(self) -> int:
        """Get the color of the hexagon."""
        return self.__color

    def __eq__(self, other: 'Hexagon') -> bool:
        """
        Check if two hexagons are equal.
        Two hexagons are considered equal if their coordinates and colors are the same.
        :param other: The other hexagon to compare.
        :return: True if the hexagons are equal, False otherwise.
        """
        return self.__x == other.get_x() and self.__y == other.get_y() and self.__color == other.get_color()
