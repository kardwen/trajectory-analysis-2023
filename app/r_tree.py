from app.trajectory import Trajectory


def buildRTree(trajectories: list[Trajectory]):
    """
    Returns an R-Tree
    """
    rTree = RTree()
    for trajectory in trajectories:
        for point in trajectory.points:
            # TODO Add point to RTree
            pass
    return rTree


class RTree:
    def __init__(self):
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
