from math import acos
from math import floor
from math import nan
from math import pow
from math import sqrt
from typing import NamedTuple

__all__ = ["Point", "calculate_distance", "Vector2D"]


class Point(NamedTuple):
    x: int
    y: int


class Vector2D(NamedTuple):
    i: int
    j: int

    @property
    def angle(self) -> float:
        if self.length == 0:
            return 0
        degree = acos((self.i) / self.length)
        if self.j < 0:
            degree *= -1
        return degree

    @property
    def length(self) -> int:
        return sqrt(pow(self.i, 2) + pow(self.j, 2))

    @property
    def norm_vector(self) -> "Vector2D":
        return Vector2D(self.i / self.length, self.j / self.length)

    @classmethod
    def from_points(cls, from_pt: Point, to_pt: Point) -> "Vector2D":
        return cls._make((b - a for b, a in zip(to_pt, from_pt)))


def calculate_distance(pt1: Point, pt2: Point) -> int:
    return floor(sqrt(pow(pt1[0] - pt2[0], 2) + pow(pt1[1] - pt2[1], 2)))
