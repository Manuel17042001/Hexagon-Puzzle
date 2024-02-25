import math

sin60 = math.sin(math.radians(60))
cos60 = 0.5


def cube_to_axial(q: int, r: int, _: int) -> tuple[int, int]:
    """
    Convert cube coordinates to axial coordinates.
    :param q: Cube coordinate q.
    :param r: Cube coordinate r.
    :param _: Cube coordinate s (unused).
    :return: Axial coordinates (x, y).
    """
    return q, r


def axial_to_cube(x: int, y: int) -> tuple[int, int, int]:
    """
    Convert axial coordinates to cube coordinates.
    :param x: Axial coordinate x.
    :param y: Axial coordinate y.
    :return: Cube coordinates (q, r, s).
    """
    return x, y, -x - y


def axial_to_oddr(x: int, y: int) -> tuple[int, int]:
    """
    Convert axial coordinates to odd-r offset coordinates.
    :param x: Axial coordinate x.
    :param y: Axial coordinate y.
    :return: Odd-r offset coordinates (x, y).
    """
    return x + int((y - (y & 1)) / 2), y


def oddr_to_axial(x: int, y: int) -> tuple[int, int]:
    """
    Convert odd-r offset coordinates to axial coordinates.
    :param x: Odd-r offset coordinate x.
    :param y: Odd-r offset coordinate y.
    :return: Axial coordinates (x, y).
    """
    return x - int((y - (y & 1)) / 2), y


def get_corner_points_of_hexagon_facing_up(center: tuple[float, float], side_length: float):
    """
    Get the corner points of a hexagon facing upward.
    :param center: Center coordinates of the hexagon.
    :param side_length: Length of each side of the hexagon.
    :return: Corner points of the hexagon.
    """
    x, y = center
    points = []
    for i in range(6):
        angle_radians = math.radians(60 * i + 90)
        x_point = x + side_length * math.cos(angle_radians)
        y_point = y + side_length * math.sin(angle_radians)
        points.append((int(x_point), int(y_point)))
    return points


def get_corner_points_of_hexagon_facing_to_side(center: tuple[float, float], side_length: float):
    """
    Get the corner points of a hexagon facing to the side.
    :param center: Center coordinates of the hexagon.
    :param side_length: Length of each side of the hexagon.
    :return: Corner points of the hexagon.
    """
    x, y = center
    points = []
    for i in range(6):
        angle_radians = math.radians(60 * i)
        x_point = x + side_length * math.cos(angle_radians)
        y_point = y + side_length * math.sin(angle_radians)
        points.append((int(x_point), int(y_point)))
    return points
