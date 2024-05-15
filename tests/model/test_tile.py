import os
import unittest

from model.hexagon import Hexagon
from model.tile import Tile


class TestTile(unittest.TestCase):

    def setUp(self):
        # Create a sample list of hexagons for testing
        hexagons = [
            Hexagon(0, 0, 0),
            Hexagon(1, 0, 0),
            Hexagon(0, 1, 0),
            Hexagon(1, 1, 0),
            Hexagon(-1, 1, 0),
            Hexagon(2, 1, 0),
        ]

        # Create a Tile object for testing
        self.tile = Tile(0, 0, hexagons)

    def test_rotate_right(self):
        self.tile.rotate(False)

        hexagons = self.tile.get_hexagons()
        assert (hexagons.__contains__(Hexagon(-1, 0, 0)))
        assert (hexagons.__contains__(Hexagon(0, 0, 0)))
        assert (hexagons.__contains__(Hexagon(-1, 1, 0)))
        assert (hexagons.__contains__(Hexagon(0, 1, 0)))
        assert (hexagons.__contains__(Hexagon(0, 2, 0)))
        assert (hexagons.__contains__(Hexagon(0, 3, 0)))

    def test_rotate_left(self):
        self.tile.rotate(True)

        hexagons = self.tile.get_hexagons()
        assert (hexagons.__contains__(Hexagon(0, -1, 0)))
        assert (hexagons.__contains__(Hexagon(1, -1, 0)))
        assert (hexagons.__contains__(Hexagon(0, 0, 0)))
        assert (hexagons.__contains__(Hexagon(1, 0, 0)))
        assert (hexagons.__contains__(Hexagon(0, 1, 0)))
        assert (hexagons.__contains__(Hexagon(2, -2, 0)))


if __name__ == '__main__':
    unittest.main()
