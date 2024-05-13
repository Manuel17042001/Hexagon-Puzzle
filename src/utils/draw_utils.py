import pygame

from utils.math_utils import get_corner_points_of_hexagon_facing_up, get_corner_points_of_hexagon_facing_to_side


def draw_hexagon_outline(surface: pygame.Surface, center: tuple[float, float], side_length: float,
                         color: tuple[int, int, int], thickness: int) -> None:
    """
    Draw the outline of a hexagon on the specified surface.
    :param surface: The surface to draw on.
    :param center: The center coordinates of the hexagon.
    :param side_length: The length of each side of the hexagon.
    :param color: The color of the hexagon outline.
    :param thickness: The thickness of the hexagon outline.
    """
    points = get_corner_points_of_hexagon_facing_up(center, side_length)
    pygame.draw.polygon(surface, color, points, thickness)


def draw_hexagon_image(surface: pygame.Surface, center: tuple[float, float], side_length: float, image) -> None:
    """
    Draw an image of a hexagon on the specified surface.
    :param surface: The surface to draw on.
    :param center: The center coordinates of the hexagon.
    :param side_length: The length of each side of the hexagon.
    :param image: The image to draw.
    """
    surface.blit(image, (center[0] - side_length, center[1] - side_length))


def draw_stretched_hexagon(surface: pygame.Surface, center: tuple[float, float], side_length: float,
                           horizontal_line_length: float, background_color: tuple[int, int, int, int],
                           line_color: tuple[int, int, int],
                           line_thickness: int) -> None:
    """
    Draw a stretched hexagon on the specified surface.
    :param surface: The surface to draw on.
    :param center: The center coordinates of the hexagon.
    :param side_length: The length of each side of the hexagon.
    :param horizontal_line_length: The length of the horizontal line to stretch the hexagon.
    :param background_color: The background color of the stretched hexagon with alpha channel.
    :param line_color: The color of the lines outlining the stretched hexagon.
    :param line_thickness: The thickness of the lines outlining the stretched hexagon.
    """

    # Create a transparent surface
    stretched_hexagon = pygame.Surface((2 * side_length + horizontal_line_length, 2 * side_length), pygame.SRCALPHA)

    # Get the points of a hexagon
    points = get_corner_points_of_hexagon_facing_to_side((side_length, side_length),
                                                         side_length)

    # Stretch the horizontal line
    points[0] = (points[0][0] + horizontal_line_length, points[0][1])
    points[1] = (points[1][0] + horizontal_line_length, points[1][1])
    points[5] = (points[5][0] + horizontal_line_length, points[5][1])

    # Draw the background and the line on the transparent surface
    pygame.draw.polygon(stretched_hexagon, background_color, points)
    pygame.draw.lines(stretched_hexagon, line_color, True, points, line_thickness)

    # Draw the stretched hexagon on the surface
    surface.blit(stretched_hexagon, (center[0] - side_length - horizontal_line_length / 2, center[1] - side_length))


def draw_rectangular_background(surface: pygame.Surface, center: tuple[float, float], width: int, height: int,
                                background_color: tuple[int, int, int, int],
                                line_color: tuple[int, int, int],
                                line_thickness: int) -> None:
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, background_color,
                     pygame.Rect(0, 0, width, height))
    pygame.draw.rect(transparent_surface, line_color,
                     pygame.Rect(0, 0, width, height), line_thickness)

    surface.blit(transparent_surface, (center[0] - width / 2, center[1] - height / 2, width, height))
