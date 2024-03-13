"""
Various utility components that do not fit elsewhere    
"""

import math

def distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Determines the distance between two points

    :param x1: X position of point 1
    :type x1: int
    :param y1: Y Position of point 1
    :type y1: int
    :param x2: X Position of point 2
    :type x2: int
    :param y2: Y position of point 2
    :type y2: int
    :return: Distance between points
    :rtype: float
    """

    return math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)


def slope(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Determines the slope between two points

    :param x1: X position of point 1
    :type x1: int
    :param y1: Y Position of point 1
    :type y1: int
    :param x2: X Position of point 2
    :type x2: int
    :param y2: Y Position of point 2
    :type y2: int
    :return: Slope between points
    :rtype: float
    """

    return (y2-y1) / (x2-x1)
