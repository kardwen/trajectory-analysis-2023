import math
from app.point import Point


class Node:
    def __init__(self, isLeaf):
        self.isLeaf: bool = isLeaf
        self.children: list[Node] = []
        self.boundingRectangle: MBR = None


class MBR:
    """Minimum Bounding Rectangle"""

    def __init__(self, minX, maxX, minY, maxY):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def contains(self, point: Point) -> bool:
        return self.minX <= point.x <= self.maxX and self.minY <= point.y <= self.maxY

    def getArea(self) -> int:
        return abs(self.maxX - self.minX) * abs(self.maxY - self.minY)


class RTree:
    """
    R-Tree

    Sources:
        (https://www.youtube.com/watch?v=hUIHtPLL940)
        Guttman, Antonin. "R-trees: A dynamic index structure for spatial searching."
        Proceedings of the 1984 ACM SIGMOD international conference on Management of data. 1984.
    """

    minEntries: int = 2
    maxEntries: int = 5

    def __init__(self, points: list[Point] = None):
        self.root = Node(True)
        if points is not None:
            # Build the R-Tree from a list of points
            for point in points:
                self.insert(point)

    def insert(self, point: Point):
        """Inserts a single point in the R-Tree"""
        # Choose leaf
        leaf = self.chooseLeaf(self.root, point)
        # TODO insert point
        # balance tree

    def chooseLeaf(self, node: Node, point: Point):
        if node.isLeaf:
            # The optimal leaf is found
            return node
        else:
            # Search for MBR that requires the least MBR area increase
            # TODO when area is equal, choose smallest area MBR
            minAreaIncrease = math.inf
            selectionIndex = 0
            for i, child in enumerate(node.children):
                areaIncrease = self.calculateAreaIncrease(node.boundingRectangle, child)
                if areaIncrease < minAreaIncrease:
                    selectionIndex = i
                    minAreaIncrease = areaIncrease
            self.chooseLeaf(node.children[selectionIndex], point)

    def calculateAreaIncrease(self, boundingRectangle: MBR, point: Point):
        # Calculate the increase in MBR area that would occur by adding the given point
        minX = min(boundingRectangle.minX, point.x)
        maxX = max(boundingRectangle.maxX, point.x)
        minY = min(boundingRectangle.minY, point.y)
        maxY = max(boundingRectangle.maxY, point.y)

        newArea = abs(maxX - minX) * abs(maxY - minY)
        increase = newArea - boundingRectangle.getArea()
        return increase
