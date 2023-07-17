from app.point import Point


class RTree:
    """
    Created after this blog post (https://www.bartoszsypytkowski.com/r-tree/)
    """

    def __init__(self, points: list[Point] = None):
        if points is not None:
            self.buildRTree(points)

    def buildRTree(self, points: list[Point]):
        """Builds the R-Tree from a list of points"""
        for point in points:
            self.insert(point)

    def insert(self, point: Point):
        """Inserts a single point in the R-Tree"""
        pass


class Node:
    def __init__(self):
        pass


class MinimumBoundingBox:
    def __init__(self, minX, maxX, minY, maxY):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def contains(self, point):
        return self.minX <= point.x <= self.maxX and self.minY <= point.y <= self.maxY
