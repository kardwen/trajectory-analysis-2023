import math
from app.point import Point


class Node:
    """
    If a node is a leaf, it contains points as children
    """

    def __init__(self, isLeaf):
        self.isLeaf: bool = isLeaf
        self.children: list[Node | Point] = []
        self.bRectangle: MBR = None
        self.parent: Node = None


class MBR:
    """Minimum Bounding Rectangle"""

    def __init__(self, minX, maxX, minY, maxY):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def contains(self, element) -> bool:
        """
        Checks if the MBR fully contains a Point or MBR element

        element: Point | MBR
        """
        if isinstance(element, Point):
            return (
                self.minX <= element.x <= self.maxX
                and self.minY <= element.y <= self.maxY
            )
        if isinstance(element, MBR):
            return (
                self.minX <= element.minX
                and element.maxX <= self.maxX
                and self.minY <= element.minY
                and element.maxY <= self.maxY
            )

    def getArea(self) -> int:
        return abs(self.maxX - self.minX) * abs(self.maxY - self.minY)

    def calculateAreaIncrease(self, point: Point):
        """Calculate the increase in MBR area that would occur by adding the given point"""
        minX = min(self.minX, point.x)
        maxX = max(self.maxX, point.x)
        minY = min(self.minY, point.y)
        maxY = max(self.maxY, point.y)

        newArea = abs(maxX - minX) * abs(maxY - minY)
        increase = newArea - self.getArea()
        return increase

    def extend(self, element):
        """Extends the MBR so that it contains the new point or MBR

        element: Point | MBR
        """
        if isinstance(element, Point):
            self.minX = min(self.minX, element.x)
            self.maxX = max(self.maxX, element.x)
            self.minY = min(self.minY, element.y)
            self.maxY = max(self.maxY, element.y)
        if isinstance(element, MBR):
            self.minX = min(self.minX, element.minX)
            self.maxX = max(self.maxX, element.maxX)
            self.minY = min(self.minY, element.minY)
            self.maxY = max(self.maxY, element.maxY)


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
        if len(leaf.children) < self.maxEntries:
            # Leaf can be extended
            leaf.children.append(point)
            # Update MBR of all affected nodes
            self.updateMBRs(leaf, point)
        else:
            # Leaf needs to be split
            pass
            # new_node, split_point = self.split_node(node, point)
            # self.adjustTree(node, new_node, split_point)

    def chooseLeaf(self, node: Node, point: Point):
        """Selects a leaf node for inserting"""
        if node.isLeaf:
            # The optimal leaf is found
            return node
        else:
            # Search for MBR that requires the least MBR area increase
            # TODO when area is equal, choose smallest area MBR
            minAreaIncrease = math.inf
            selectionIndex = 0
            for i, child in enumerate(node.children):
                areaIncrease = child.bRectangle.calculateAreaIncrease(point)
                if areaIncrease < minAreaIncrease:
                    selectionIndex = i
                    minAreaIncrease = areaIncrease
            self.chooseLeaf(node.children[selectionIndex], point)

    def updateMBRs(self, node: Node, element: Point | MBR):
        """
        Check if the bounding box needs to be extended,
        recursively checks parent nodes
        """
        # If no MBR is set, the root is reached
        if node.bRectangle is not None:
            if node.bRectangle.contains(element):
                # MBR does not need to be updated
                return
            # Adjust MBR size
            node.bRectangle.extend(element)
            if node.parent is not None:
                # Continue with adjusting the size of the parent node
                self.updateMBRs(node.parent, node.bRectangle)
