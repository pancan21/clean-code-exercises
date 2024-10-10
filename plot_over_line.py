# This code contains a `PointCloud` class that lets you
# store a number of points and retrieve the nearest neighbor
# point of the point cloud for any given point.
#
# Then, we have the function `plot_over_line` to plot a discrete
# function - defined by values on the points of the point cloud -
# along a given line with a specified number of samples along the line.
# To this end, the nearest neighbor in the point cloud for each point
# on the line is determined, and that closest discrete function value
# is chosen for plotting.
#
# There are several "issues" with this implementation. First of all, there
# is a poorly named argument in the `plot_over_line` function. But there is
# much more that can be improved. Try to clean this code up and look into
# `plot_over_line_hints.py` for hints on where to start.

from __future__ import annotations
from typing import List
from dataclasses import dataclass
from math import pi, sqrt, sin, cos
from matplotlib.pyplot import plot, show, close


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return sqrt(dx*dx + dy*dy)


class PointCloud:
    def __init__(self, points: List[Point]) -> None:
        self._points = points

    @property
    def size(self) -> int:
        return len(self._points)

    # This is to make a `PointCloud` iterable, that is, to
    # allow looping over its points like this:
    #
    # for p in point_cloud:
    #     ...
    def __iter__(self):
        return iter(self._points)

    def __getitem__(self, index: int) -> Point:
        return self._points[index]

    def get_nearest(self, p: Point) -> Point:
        # Note: this is very inefficient, but does it for us...
        return min(self._points, key=lambda point: point.distance_to(p))

    def get_nearest_point_index(self, p: Point) -> int:
        # Note: this is very inefficient, but does it for us...
        return self._points.index(self.get_nearest(p))

class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self._start = start
        self._end = end
        self._vector = (
            end.x - start.x,
            end.y - start.y
        )

    @property
    def source(self) -> Point:
        return self._start

    @property
    def target(self) -> Point:
        return self._end

    def at(self, fraction: float) -> Point:
        assert fraction >= 0.0 and fraction <= 1.0
        return Point(
            self._start.x + fraction*self._vector[0],
            self._start.y + fraction*self._vector[1]
        )

    def get_points_on_line(self, num_points: int) -> List[Point]:
        '''let us discretize the line into `num_points` points'''
        dx = (self._end.x - self._start.x)/(num_points - 1)
        dy = (self._end.y - self._start.y)/(num_points - 1)
        return [Point(self._start.x + dx*float(i), self._start.y + dy*float(i)) for i in range(num_points)]

def plot_over_line(point_cloud: PointCloud,
                   point_values: List[float],
                   line: Line,
                   num_points: int) -> None:
    assert point_cloud.size == len(point_values)

    points_on_line = line.get_points_on_line(num_points)

    x = []
    y = []
    for i in range(num_points):
        current = points_on_line[i]
        x.append(line._start.distance_to(current))
        y.append(point_values[point_cloud.get_nearest_point_index(current)])

    plot(x, y)
    show()
    close()


def _test_function(position: Point) -> float:
    return sin(2.0*pi*position.x)*cos(2.0*pi*position.y)


if __name__ == "__main__":
    print("Plotting along a line though a point cloud...")
    print(
        "Note that this may take some time since we are "
        "doing a brute force nearest neighbor evaluation"
    )

    domain_size = (1.0, 1.0)
    number_of_points = (50, 50)
    dx = (
        domain_size[0]/float(number_of_points[0]),
        domain_size[1]/float(number_of_points[1])
    )

    point_cloud = PointCloud([
        Point(float(i)*dx[0], float(j)*dx[1])
        for i in range(number_of_points[0])
        for j in range(number_of_points[1])
    ])

    point_values = [_test_function(p) for p in point_cloud]
    
    line = Line(Point(0.0, 0.0), Point(1.0, 1.0))

    plot_over_line(
        point_cloud,
        point_values,
        line,
        num_points=2000
    )
