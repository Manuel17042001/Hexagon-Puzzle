import random
from copy import deepcopy

import numpy as np

from model.hexagon import Hexagon
from model.tile import Tile


def get_neighbour_coordinates(x: int, y: int, n: int):
    """
    Calculates the coordinates of a neighboring cell in a hexagonal grid.

    :param x: Current x-coordinate.
    :param y: Current y-coordinate.
    :param n: Neighbor index (0 to 5 inclusive).

    :return: Coordinates of the neighboring cell as a tuple (int, int).

    :raises AssertionError: If the neighbor index is not in the range [0, 5].
    """
    assert 0 <= n <= 5, "The index of the neighbours has to be between 0 and 5"

    even_row_neighbors = {
        0: (x - 1, y - 1),
        1: (x, y - 1),
        2: (x + 1, y),
        3: (x, y + 1),
        4: (x - 1, y + 1),
        5: (x - 1, y)
    }

    odd_row_neighbors = {
        0: (x, y - 1),
        1: (x + 1, y - 1),
        2: (x + 1, y),
        3: (x + 1, y + 1),
        4: (x, y + 1),
        5: (x - 1, y)
    }

    if y % 2 == 0:
        return even_row_neighbors[n]
    else:
        return odd_row_neighbors[n]


class HexagonalMap(object):

    def __init__(self, width: int, height: int):
        """
        Initialize a hexagonal map with the specified width and height.
        :param width: The width of the map (must be greater than or equal to 3).
        :param height: The height of the map (must be greater than or equal to 3).
        """
        assert width >= 3 and height >= 3, "Width and height have to be greater or equal to 3"
        self.__width = width + 2  # add two for the border on the left and right
        self.__height = height + 2  # add two for the border on the top and bottom
        self.__generate_map()  # generate map with constrains
        self.__puzzle_map = None
        self.__tiles = self.generate_puzzle()
        self.__actual_map = [[None for _ in range(self.__width)] for _ in range(self.__height)]

    def get_grid_size(self) -> (int, int):
        return self.__width - 2, self.__height - 2

    def get_tiles(self) -> list:
        return self.__tiles

    def get_actual_map(self) -> list:
        return self.__actual_map

    def set_actual_map(self, actual_map: list):
        self.__actual_map = actual_map

    def __remove_single_islands(self) -> None:
        for x in range(self.__width):
            for y in range(self.__height):
                if self._map[x][y] == 0:
                    continue
                if self.__check_is_single_island(x, y):
                    self._map[x][y] = 0

    def __check_is_single_island(self, x: int, y: int) -> bool:
        is_single_island = True
        for x_neighbour, y_neighbour in [get_neighbour_coordinates(x, y, i) for i in [0, 1, 2, 3, 4, 5]]:
            if self._map[x_neighbour][y_neighbour] == 1:
                is_single_island = False
                break
        return is_single_island

    def __generate_map(self) -> None:
        """
        Generate the hexagonal map with one single connected island, consisting of a border of zeros and a random map
        with zeros and ones.
        """
        # generate random Map with border 0
        self._map = [[random.choice([0, 1]) if 0 < y < self.__height - 1 and 0 < x < self.__width - 1 else 0
                      for y in range(self.__height)]
                     for x in range(self.__width)]

        # remove single islands
        self.__remove_single_islands()

        # connect the islands to one big island
        self.__connect_islands()

    def __connect_islands(self) -> None:
        # FIXME change code if islands are more than one hexagon away
        def set_value_to_island(map, x, y, value):
            map[x][y] = value
            for x, y in [get_neighbour_coordinates(x, y, k) for k in [0, 1, 2, 3, 4, 5]]:
                if map[x][y] == 1:
                    set_value_to_island(map, x, y, value)

        # take a copy of the map
        map_tmp = deepcopy(self._map)

        n_island = 2

        # set the hexagons from one island to the same value
        for i in range(self.__width):
            for j in range(self.__height):
                if map_tmp[i][j] == 1:
                    set_value_to_island(map_tmp, i, j, n_island)
                    n_island += 1

        # set the water-hexagons to the value of the different neighbour island count
        for i in range(1, self.__width - 1):
            for j in range(1, self.__height - 1):
                set_islands = []
                if map_tmp[i][j] == 0:
                    for x, y in [get_neighbour_coordinates(i, j, k) for k in [0, 1, 2, 3, 4, 5]]:
                        if map_tmp[x][y] > 0:
                            if not set_islands.__contains__(map_tmp[x][y]):
                                set_islands.append(map_tmp[x][y])
                    map_tmp[i][j] = -len(set_islands)

        # select the hexagons with the most neighbour island
        max_tiles = []
        max_value = -2
        for i in range(1, self.__width - 1):
            for j in range(1, self.__height - 1):
                if map_tmp[i][j] == max_value:
                    max_tiles.append((i, j))
                    max_tiles = [(i, j)]

        # select randomly one of the hexagons with the most neighbours and set it to 1
        if len(max_tiles):
            x, y = random.choice(max_tiles)
            self._map[x][y] = 1
            self.__connect_islands()

    def generate_tile(self, x: int, y: int, count: int, tile_n: int) -> int:
        if self.__puzzle_map[x][y] == 0:
            self.__puzzle_map[x][y] = tile_n
            count = count - 1
            edges = [0, 1, 2, 3, 4, 5]
            while count > 0 and len(edges) > 0:
                edge = random.choice(edges)
                edges.remove(edge)
                x_neighbour, y_neighbour = (get_neighbour_coordinates(x, y, edge))
                count = self.generate_tile(x_neighbour, y_neighbour, count, tile_n)
        return count

    def generate_puzzle(self):
        # create a map with borders -1
        self.__puzzle_map = [[0 if 0 < y < self.__height - 1 and 0 < x < self.__width - 1 else -1
                              for y in range(self.__height)]
                             for x in range(self.__width)]

        tile_n = 1  # the current number of the tile

        for i in range(1, self.__width - 1):
            for j in range(1, self.__height - 1):
                if self.__puzzle_map[i][j] == 0:
                    self.generate_tile(i, j, random.choice(range(2, 7)), tile_n)
                    tile_n += 1

        tiles = [Tile(900, 200, []) for _ in range(np.max(self.__puzzle_map))]

        for x in range(1, self.__width - 1):
            for y in range(1, self.__height - 1):
                value = self.__puzzle_map[x][y] - 1
                if value >= 0:
                    tiles[value].get_hexagons().append(Hexagon(x, y, self._map[x][y]))

        for tile in tiles:
            tile.normalise_hexagon_pos()
            if random.random() < 0.33:
                tile.flip_horizontal()
            elif random.random() < 0.66:
                tile.flip_vertical()
            rotation = int(random.random() / 6) - 3
            while rotation != 0:
                if rotation < 0:
                    tile.rotate(False)
                    rotation += 1
                elif rotation > 0:
                    tile.rotate(True)

        return tiles
