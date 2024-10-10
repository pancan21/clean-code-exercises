# The `RasterGrid` represents a structured, rectangular grid in 2d space.
# Each cell of the grid is identified by its column/row index pair:
#
#  ________ ________ ________
# |        |        |        |
# | (0, 1) | (1, 1) | (2, 2) |
# |________|________|________|
# |        |        |        |
# | (0, 0) | (1, 0) | (2, 0) |
# |________|________|________|
#
#
# One can construct a `RasterGrid` by specifying the lower left and upper right
# corners of a domain and the number of cells one wants to use in x- and y-directions.
# Then, `RasterGrid` allows to iterate over all cells and retrieve the center point
# of that cell.
#
# This class can be significantly cleaned up, though. Give it a try, and if you need
# help you may look into the file `raster_grid_hints.py`.
# Make sure to make small changes, verifying that the test still passes, and put
# each small change into a separate commit.
from typing import Tuple
from math import isclose
from dataclasses import dataclass

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(self,
                 lower_left: Point,
                 upper_right: Point,
                 nx: int,
                 ny: int) -> None:
        self._lower_left = lower_left
        self._upper_right = upper_right
        self._nx = nx
        self._ny = ny
        self.num_cells = nx*ny
        self.cells = [
            self.Cell(i, j) for i in range(nx) for j in range(ny)
        ]

    def calculate_cell_center(self, cell: Cell) -> Tuple[float, float]:
        return (
            self._lower_left.x + (self._upper_right.x - self._lower_left.x)*(cell._ix + 0.5)/self._nx,
            self._lower_left.y + (self._upper_right.y - self._lower_left.y)*(cell._iy + 0.5)/self._ny
        )


def test_number_of_cells():
    x0 = 0.0
    y0 = 0.0
    dx = 1.0
    dy = 1.0
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 10, 10).num_cells == 100
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 10, 20).num_cells == 200
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 20, 10).num_cells == 200
    assert RasterGrid(Point(x0, y0), Point(dx, dy), 20, 20).num_cells == 400


def test_cell_center():
    grid = RasterGrid(Point(0.0, 0.0), Point(2.0, 2.0), 2, 2)
    expected_centers = [
        (0.5, 0.5),
        (1.5, 0.5),
        (0.5, 1.5),
        (1.5, 1.5)
    ]

    for cell in grid.cells:
        for center in expected_centers:
            if isclose(grid.calculate_cell_center(cell)[0], center[0]) and isclose(grid.calculate_cell_center(cell)[1], center[1]):
                expected_centers.remove(center)

    assert len(expected_centers) == 0


if __name__ == "__main__":
    test_number_of_cells()
    test_cell_center()
    print("All tests passed")
