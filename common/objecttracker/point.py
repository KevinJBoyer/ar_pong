from math import sqrt


class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y

        return False

    def distance_to(self, other: "Point") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def interpolate_toward(self, destination: "Point", speed: float) -> "Point":
        return Point(
            self.x + ((destination.x - self.x) * speed),
            self.y + ((destination.y - self.y) * speed),
        )

    def closest_to(self, coords: list["Point"]) -> "Point":
        closest_point = coords[0]
        smallest_distance = self.distance_to(coords[0])

        for coord in coords[1:]:
            distance = self.distance_to(coord)
            if distance < smallest_distance:
                closest_point = coord
                smallest_distance = distance

        return closest_point
