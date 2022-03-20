from math import sqrt
from typing import NamedTuple
from typing_extensions import TypeAlias

# todo: add unit tests

Point = NamedTuple("Point", [("x", float), ("y", float)])
Distance: TypeAlias = float
CoordsIndex: TypeAlias = int


def dist(p1: Point, p2: Point) -> Distance:
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def interpolate(origin: Point, destination: Point, speed: float) -> Point:
    d_x = destination.x - origin.x
    d_y = destination.y - origin.y

    return Point(
        origin.x + (d_x * speed),
        origin.y + (d_y * speed),
    )


def closest_to(point: Point, coords: list[Point]) -> Point:
    closest_point = coords[0]
    smallest_distance = dist(point, coords[0])

    for coord in coords[1:]:
        distance = dist(point, coord)
        if distance < smallest_distance:
            closest_point = coord
            smallest_distance = distance

    return closest_point
