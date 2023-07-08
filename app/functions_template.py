from app.trajectory import Trajectory
from app.point import Point
from app.region import Region
from app import utils


def douglasPeucker(traj: Trajectory, epsilon: float) -> Trajectory:
    """
    Returns a simplified trajectory with the same number attribute
    """
    points = traj.points
    # Simply return invalid trajectories for now
    if len(points) < 2:
        return Trajectory(traj.number, traj.points)
    maxDist = 0
    index = 0
    end = len(points) - 1
    # Regard all points between the start and end point
    for i in range(1, end - 1):
        # Find the point furthest away from a straight line between start and end
        dist = utils.calculateDistance(points[i], points[0], points[end])
        if dist > maxDist:
            index = i
            maxDist = dist
    if maxDist > epsilon:
        resultPartA = douglasPeucker(
            Trajectory(traj.number, points[0 : index + 1]), epsilon
        )
        resultPartB = douglasPeucker(Trajectory(traj.number, points[index:]), epsilon)
        return Trajectory(traj.number, resultPartA.points[0:-1] + resultPartB.points)
    else:
        return Trajectory(traj.number, [points[0], points[end]])


def slidingWindow(traj: Trajectory, epsilon) -> Trajectory:
    """
    Returns a simplified trajectory with the same number attribute
    Before Open Window algoritm
    """
    points = traj.points
    simplified = [points[0]]
    leftWindowBorder = 0  # anchor
    rightWindowBorder = 2

    while rightWindowBorder < len(points):
        # Check if the maximal distance of each point of the window to the
        # new segment that would be created by this window is smaller than epsilon
        for j in range(leftWindowBorder + 1, rightWindowBorder):
            dist = utils.calculateDistance(
                points[j], points[leftWindowBorder], points[rightWindowBorder]
            )
            if dist > epsilon:
                # Shift window
                leftWindowBorder = rightWindowBorder - 1
                simplified.append(points[rightWindowBorder - 1])
                rightWindowBorder = leftWindowBorder + 2
                break
            if j == rightWindowBorder - 1:
                # Extend window
                rightWindowBorder += 1

    # Always include the last point of the original trajectory
    simplified.append(points[-1])

    return Trajectory(traj.number, simplified)


def closestPairDistance(traj0: Trajectory, traj1: Trajectory) -> float:
    # TODO
    return 0.0


def dynamicTimeWarping(traj0: Trajectory, traj1: Trajectory) -> float:
    # TODO
    return 0.0


def solveQueryWithRTree(r: Region, trajectories: list) -> list:
    # TODO
    return []


def solveQueryWithoutRTree(r: Region, trajectories: list) -> list:
    # TODO
    return []
