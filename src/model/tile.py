from model.hexagon import Hexagon
from utils import math_utils


class Tile(object):

    def __init__(self, pos_x: float, pos_y: float, hexagons: list[Hexagon]):
        """
        Initialize the Tile with position and hexagons.

        Parameters:
        :param pos_x: The x-coordinate of the tile position, respecting the first hexagon.
        :param pos_y: The y-coordinate of the tile position, respecting the first hexagon.
        :param hexagons: The list of hexagons of the tile.
        """
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__hexagons = hexagons
        self.__grid_pos = None

    def get_pos_x(self) -> float:
        """Get the x-coordinate of the tile."""
        return self.__pos_x

    def set_pos_x(self, pos_x: float) -> None:
        """Set the x-coordinate of the tile."""
        self.__pos_x = pos_x

    def get_pos_y(self) -> float:
        """Get the y-coordinate of the tile."""
        return self.__pos_y

    def get_position(self) -> tuple[float, float]:
        """Get the position of the tile as a tuple of (x, y) coordinates."""
        return self.__pos_x, self.__pos_y

    def set_pos_y(self, pos_y: float) -> None:
        """Set the y-coordinate of the tile."""
        self.__pos_y = pos_y

    def get_hexagons(self) -> list[Hexagon]:
        """Get the list of hexagons of the tile"""
        return self.__hexagons

    def get_grid_pos(self) -> (int, int):
        """Get the grid position of the tile."""
        return self.__grid_pos

    def set_grid_pos(self, pos: (int, int)) -> None:
        """Set the grid position of the tile."""
        self.__grid_pos = pos

    def normalise_hexagon_pos(self):
        """
        Normalize the position of hexagons such that the first hexagon's coordinates become (0, 0).
        """
        # Get a reference to the list of hexagons
        hexagons = self.__hexagons

        # Get the coordinates of the first hexagon
        hexagon_0_x, hexagon_0_y = hexagons[0].get_coordinates()

        # If the first hexagon is already at (0, 0), return
        if hexagon_0_x == 0 and hexagon_0_y == 0:
            return

        # Iterate through each hexagon to adjust its coordinates
        for hexagon in hexagons:
            # Calculate the new coordinates relative to the first hexagon
            new_y = hexagon.get_y() - hexagon_0_y
            new_x = hexagon.get_x() - hexagon_0_x - (0 if hexagon_0_y % 2 == 0 else new_y % 2)
            # Set the new coordinates for the hexagon
            hexagon.set_coordinates(new_x, new_y)

    def flip_vertical(self) -> None:
        """
        Flip hexagons vertically.
        """
        for hexagon in self.__hexagons:
            hexagon.set_y(-hexagon.get_y())

    def flip_horizontal(self) -> None:
        """
        Flip hexagons horizontally.
        """
        for hexagon in self.__hexagons:
            hexagon.set_x(-hexagon.get_x() - hexagon.get_y() % 2)

    def rotate(self, direction: bool) -> None:
        """
        Rotate hexagons either clockwise or counterclockwise based on the direction.
        :param direction: True for clockwise, False for counterclockwise
        """
        for hexagon in self.__hexagons:
            # Get coordinates of the hexagon
            x, y = hexagon.get_coordinates()

            # Convert the coordinates
            x, y = math_utils.oddr_to_axial(x, y)
            q, r, s = math_utils.axial_to_cube(x, y)

            # Rotate cube coordinates based on the direction
            if direction:
                q, r, s = -s, -q, -r  # Clockwise rotation
            else:
                q, r, s = -r, -s, -q  # Counterclockwise rotation

            # Convert the coordinates back
            x, y = math_utils.cube_to_axial(q, r, s)
            x, y = math_utils.axial_to_oddr(x, y)

            # Set the new coordinates for the hexagon
            hexagon.set_x(x)
            hexagon.set_y(y)
