# Hint 1:
# `plot_over_line` does the discretization of the line into `n` points, which could be
# something that is useful in other contexts. We should maybe put that into a reusable
# functionality. One idea could be to introduce a `Line` of `Segment` class that allows
# to retrieve points between its source and target points being given a fraction between
# 0 and 1.0, where at 0.0 we would obtain the source point, and at 1.0 we would obtain
# the target point. This way we could combine the two point arguments in `plot_over_line`
# into a single argument.


# Hint 2:
# Such a `Line` class could look like this:
#
# class Line:
#     def __init__(self, source: Point, target: Point) -> None:
#         self._source = source
#         self._target = target
#         self._vector = (
#             target.x - source.x,
#             target.y - source.y
#         )
#
#     @property
#     def source(self) -> Point:
#         return self._source
#
#     @property
#     def target(self) -> Point:
#         return self._target
#
#     def at(self, fraction: float) -> Point:
#         assert fraction >= 0.0 and fraction <= 1.0
#         return Point(
#             self._source.x + fraction*self._vector[0],
#             self._source.y + fraction*self._vector[1]
#         )


# Hint 3:
# It would be nice if one could generate the plot data independent of
# the actual plotting so that you can use the plot data in a different
# context. Try to separate the plot data generation from `plot_over_line`
# into a separate functionality.


# Hint 4:
# `plot_over_line` receives the point cloud and the discrete
# values separately, and then internally it looks for the nearest
# neighbor (by means of the index). Thus, `plot_over_line` currently decides
# how to interpolate the values, although its primary concern should
# simply be plotting. Can we maybe combine a `PointCloud` and the
# discrete values into something that represents a discrete function
# that can be evaluated at a given point? Then we could put the
# knowledge of how to interpolate inside the point cloud in there,
# and not in `plot_over_line`, which shouldn't be doing such thing.
#
# Note: to make an object callable, you have to implement the __call__
#       operator:
#
# class MyClass:
#     def __call__(self, some_argument: SOME_ARGUMENT_TYPE) -> SOME_RETURN_TYPE:
#         return ...


# Hint 5:
# You can maybe combine the point cloud and the point values into a `DiscreteFunction`
# that looks something like this:
#
# class DiscreteFunction:
#     def __init__(self, point_cloud: PointCloud, point_values: List[float]) -> None:
#         ...
#
#     def __call__(self, point: Point) -> float:
#         return self._values[self._point_cloud.get_nearest_neighbor_index(point)]
