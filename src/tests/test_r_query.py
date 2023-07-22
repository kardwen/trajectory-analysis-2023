from app.functions import solveQueryWithRTree
from app.point import Point
from app.r_tree import RTree
from app.region import Region
from app.trajectory import Trajectory


def testRTreeInsertionAndQuery():
    """
    Test R-tree insertion and query functionality
    """
    # Create an R-tree
    tree = RTree()

    trajectoryA = Trajectory(
        0,
        [
            Point(0.1, 0.2, "2000-01-01 01:18:21"),
            Point(0.5, 0.7, "2000-01-01 01:18:22"),
            Point(0.8, 0.5, "2000-01-01 01:18:23"),
            Point(1.0, 2.0, "2000-01-01 01:18:21"),
            Point(3.0, 2.4, "2000-01-01 01:18:22"),
            Point(4.0, 2.2, "2000-01-01 01:18:23"),
            Point(7.0, 2.7, "2000-01-01 01:18:24"),
        ],
    )
    trajectoryB = Trajectory(
        1,
        [
            Point(0.1, 0.1, "2000-01-01 01:18:21"),
            Point(2.5, 0.4, "2000-01-01 01:18:22"),
            Point(4.0, 0.9, "2000-01-01 01:18:23"),
            Point(6.0, 0.5, "2000-01-01 01:18:23"),
        ],
    )
    trajectories = [trajectoryA, trajectoryB]

    for trajectory in trajectories:
        for point in trajectory.points:
            tree.insert(point)
    queryRegion = Region(Point(4.0, 1.0, "2000-01-01 01:18:25"), 0.5)

    queryResult = solveQueryWithRTree(queryRegion, tree, trajectories)

    print(queryResult[0])
    # This query should yield only the second trajectory
    assert [trajectory.number for trajectory in queryResult] == [trajectoryB.number]
