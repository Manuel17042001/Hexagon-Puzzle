import random
from copy import deepcopy

import numpy as np

from model.hexagon import Hexagon
from model.screen_data import ScreenData
from model.tile import Tile
from utils.math_utils import get_neighbour_coordinates


class HexagonalMap(object):

    def __init__(self, width: int, height: int, fixed_tiles: float):
        """
        Initialize a hexagonal map with the specified width and height.
        :param width: The width of the map (must be greater than or equal to 3).
        :param height: The height of the map (must be greater than or equal to 3).
        :param fixed_tiles: Whether the map has fixed tiles or not.
        """
        assert width >= 3 and height >= 3, "Width and height have to be greater or equal to 3"
        self.__width = width + 2  # add two for the border on the left and right
        self.__height = height + 2  # add two for the border on the top and bottom
        self.__generate_map()  # generate map with constrains
        self.__puzzle_map = None
        self.__fixed_tiles = fixed_tiles
        self.__actual_map = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        self.__tiles = self.generate_puzzle()

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
        def set_value_to_island(map, x, y, value):
            map[x][y] = (1, value, 0)
            for x_n, y_n in [get_neighbour_coordinates(x, y, k) for k in [0, 1, 2, 3, 4, 5]]:
                if map[x_n][y_n] == 1:
                    set_value_to_island(map, x_n, y_n, value)

        tmp_map = deepcopy(self._map)

        num_island = 1

        # set the hexagons from one island to the same value
        for i in range(self.__width):
            for j in range(self.__height):
                if tmp_map[i][j] == 1:
                    set_value_to_island(tmp_map, i, j, num_island)
                    num_island += 1

        all_calculated = False
        while not all_calculated:
            all_calculated = True
            for i in range(1, self.__width - 1):
                for j in range(1, self.__height - 1):
                    if tmp_map[i][j] == 0:
                        for x, y in [get_neighbour_coordinates(i, j, k) for k in [0, 1, 2, 3, 4, 5]]:
                            if 0 < x < self.__width - 1 and 0 < y < self.__height - 1:
                                tmp_map_xy = tmp_map[x][y]
                                if isinstance(tmp_map_xy, tuple):
                                    if isinstance(tmp_map[i][j], tuple):
                                        if tmp_map[i][j][2] < tmp_map_xy[2] + 1:
                                            continue
                                        else:
                                            tmp_map[i][j] = (0, tmp_map_xy[1], tmp_map_xy[2] + 1)
                                    else:
                                        tmp_map[i][j] = (0, tmp_map_xy[1], tmp_map_xy[2] + 1)
                                    all_calculated = False

        borders = []

        for i in range(num_island):
            borders.append([])
            for _ in range(num_island - i):
                borders[-1].append([])

        for i in range(1, self.__width - 1):
            for j in range(1, self.__height - 1):
                for x, y in [get_neighbour_coordinates(i, j, k) for k in [0, 1, 2]]:
                    if 0 < x < self.__width - 1 and 0 < y < self.__height - 1:
                        i_hexagon = tmp_map[i][j][1]
                        i_neighbour = tmp_map[x][y][1]
                        if i_hexagon != i_neighbour:
                            borders[min(i_hexagon, i_neighbour) - 1][max(i_hexagon, i_neighbour) - 1].append(
                                ((i, j, tmp_map[i][j][2]), (x, y, tmp_map[x][y][2])))

        nearest_borders = []
        for row in borders:
            for list in row:
                if list:
                    nearest_borders.append([])
                    min_i = self.__width * self.__height
                    for border in list:
                        b1 = border[0][2]
                        b2 = border[1][2]
                        if min_i > b1 + b2:
                            nearest_borders[-1] = []
                            min_i = b1 + b2
                        elif min_i < b1 + b2:
                            continue
                        nearest_borders[-1].append(border)

        def connect_to_island(map, x, y):
            color, island, distance = map[x][y]
            if color == 0 and distance > 0:
                map[x][y] = (1, map[x][y][1], map[x][y][2])
                list_hex = []
                for i, j in [get_neighbour_coordinates(x, y, k) for k in [0, 1, 2, 3, 4, 5]]:
                    if 0 < i < self.__width - 1 and 0 < j < self.__height - 1:
                        neighbour = map[i][j]
                        if neighbour[1] == island and neighbour[2] == distance - 1:
                            list_hex.append((x, y))
                choice = list_hex[random.randint(0, len(list_hex) - 1)]
                connect_to_island(map, choice[0], choice[1])

        for borders in nearest_borders:
            border_choice = borders[random.randint(0, len(borders) - 1)]
            for hexagon in border_choice:
                x, y = hexagon[0], hexagon[1]
                connect_to_island(tmp_map, x, y)

        new_map = [[tmp_map[i][j][0] if 0 < j < self.__height - 1 and 0 < i < self.__width - 1 else 0 for j in
                    range(self.__height)] for i in range(self.__width)]

        self._map = new_map

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

        window_width, window_height = ScreenData().get_window().get_size()

        tiles = [
            Tile(window_width * 3 / 4, window_height * 3 / 8, [])
            for _ in range(np.max(self.__puzzle_map))]

        for x in range(1, self.__width - 1):
            for y in range(1, self.__height - 1):
                value = self.__puzzle_map[x][y] - 1
                if value >= 0:
                    tiles[value].get_hexagons().append(Hexagon(x, y, self._map[x][y]))

        for tile in tiles:
            if random.random() < self.__fixed_tiles:
                tile.set_moveable(False)
                for hexagon in tile.get_hexagons():
                    x, y = hexagon.get_coordinates()
                    self.__actual_map[y][x] = hexagon.get_color()
                tile.set_grid_pos(tile.get_hexagons()[0].get_coordinates())
                continue
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

    def is_puzzle_correctly(self):
        def set_value_to_island(map, x, y, value):
            map[x][y] = value
            for y_n, x_n in [get_neighbour_coordinates(y, x, k) for k in [0, 1, 2, 3, 4, 5]]:
                if map[x_n][y_n] == 1:
                    set_value_to_island(map, x_n, y_n, value)

        num_islands = 1

        tmp_map = deepcopy(self.__actual_map)

        for i in range(1, self.__height - 1):
            for j in range(1, self.__width - 1):
                if tmp_map[i][j] is None:
                    return False
                elif tmp_map[i][j] == 0:
                    continue
                elif tmp_map[i][j] == 1 and num_islands == 1:
                    set_value_to_island(tmp_map, i, j, 0)
                    num_islands += 1
                else:
                    return False
        return True
