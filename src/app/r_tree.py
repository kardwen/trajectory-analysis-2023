import math

from app.point import Point


class Node:
    """
    Node

    If a node is a leaf, it contains points as children.
    """

    def __init__(self, isLeaf: bool):
        self.isLeaf: bool = isLeaf
        self.children: list[Node | Point] = []
        self.parent: Node = None
        self.mbr: MBR = None

    def updateMBR(self):
        """Updates the bounding rectangle so that it contains all children"""
        if len(self.children) == 0:
            self.mbr = None
            return
        if self.isLeaf:  # Calculate MBR of all points
            minX = min(point.x for point in self.children)
            maxX = max(point.x for point in self.children)
            minX = min(point.y for point in self.children)
            maxY = max(point.y for point in self.children)
        else:  # Calculate MBR from child nodes MBR
            minX = min(node.mbr.minX for node in self.children)
            maxX = max(node.mbr.maxX for node in self.children)
            minX = min(node.mbr.minY for node in self.children)
            maxY = max(node.mbr.maxY for node in self.children)
        self.mbr = MBR(minX, maxX, minX, maxY)


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
        """Calculate the increase in MBR area that would result by adding the given point"""
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
        leaf: Node = self.chooseLeaf(self.root, point)
        if len(leaf.children) < self.maxEntries:
            # Leaf can be extended
            leaf.children.append(point)
            # Update MBR of all affected nodes
            self.adjustTree(leaf, point)
        else:
            # Leaf needs to be split
            self.splitNode(leaf, point)

    def chooseLeaf(self, node: Node, point: Point) -> Node:
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
                areaIncrease = child.mbr.calculateAreaIncrease(point)
                if areaIncrease < minAreaIncrease:
                    selectionIndex = i
                    minAreaIncrease = areaIncrease
            return self.chooseLeaf(node.children[selectionIndex], point)

    def splitNode(self, node: Node, element: Point | Node):
        """
        Splits a node by assigning parts of its children to a newly created node
        and inserting a new node
        """
        if len(node.children) < self.maxEntries:
            # no split needed, simply update children and MBR
            node.children.append(element)
            self.adjustTree(node, element)
            return

        # If the root node needs to be split a new root has to be created
        if not node.parent:
            root = Node(False)
            node.parent = root
            self.root = root
            root.children.append(node)

        # Linear split of children in the middle for now
        # TODO implement quadratic cost function
        splitIndex = len(node.children) // 2
        # Create a new node
        newNode = Node(node.isLeaf)
        newNode.children = node.children[splitIndex:]
        for child in newNode.children:
            child.parent = newNode
        newNode.parent = node.parent
        # Update existing node
        node.children = node.children[:splitIndex]
        # Update MBR
        node.updateMBR()
        newNode.updateMBR()

        # Add new element to one of the two nodes
        # TODO choose best node for adding element (in quadratic cost function)
        node.children.append(element)
        if isinstance(element, Node):
            # if the added element is a node, also update its parent reference
            element.parent = node
        node.updateMBR()

        # Register the new node in the parent node
        self.splitNode(node.parent, newNode)

    def quadraticCost(self):
        # TODO
        # if node.isLeaf:
        #     # Choose two nodes that would cause the largest area as starting nodes
        #     maxIncrease = 0
        #     foundPair = (0, 0)
        #     for i in range(0, len(node.children) - 1):
        #         # Pair-wise comparison
        #         pointA = node.children[i]
        #         for j in range(i + 1, len(node.children)):
        #             pointB = node.children[j]
        #             increase = abs(pointA.x - pointB.x) * abs(pointA.y - pointB.y)
        #             if increase > maxIncrease:
        #                 maxIncrease = increase
        #                 foundPair = (i, j)
        #     # Assign other points
        #     for i in range(0, len(node.children)):
        #         if i in foundPair:
        #             continue
        pass

    def adjustTree(self, node: Node, element: Point | MBR):
        """
        Check if the bounding box needs to be extended,
        recursively checks parent nodes
        """
        if not node.mbr:
            # Calculate MBR if none is set, which is the case for the root
            node.updateMBR()
            return
        # MBR does not need to be updated if the element is already contained
        if node.mbr.contains(element):
            return
        # Update MBR
        node.updateMBR()
        # Continue with adjusting the parent node
        if node.parent is not None:
            self.adjustTree(node.parent, node.mbr)
