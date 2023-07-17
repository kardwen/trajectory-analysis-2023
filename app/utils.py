import math
from glob import glob
import numpy as np

from app.point import Point
from app.trajectory import Trajectory


def importTrajectory(filename: str, number: int) -> Trajectory:
    """Import a single trajectory from a file with the file format
    xCoordinate yCoordinate day hour ... (other attributes will
    not be imported).
    Each trajectory should hold an unique number (id)."""

    # Import
    data = np.loadtxt(filename, delimiter=" ", dtype=str)

    # Create trajectory
    currTrajectory = Trajectory(number)

    # Convert data into points
    for entry in data:
        # Create point
        x = float(entry[0])
        y = float(entry[1])
        day = entry[2]
        hour = entry[3]
        timestamp = day + ":" + hour
        newPoint = Point(x, y, timestamp, currTrajectory.number)
        currTrajectory.addPoint(newPoint)

    # Return trajectory
    return currTrajectory


def importTrajectories(foldername: str) -> list[Trajectory]:
    """Import the given set of 62 with indexes between 1 and 96 trajectories"""

    listOfTrajectories = []
    for i in range(1, 96):
        filename = foldername + "/extractedTrace" + str(i) + ".txt"

        if glob(filename):
            currTrajectory = importTrajectory(filename, i)
            listOfTrajectories.append(currTrajectory)
    return listOfTrajectories


def calculateDistance(point: Point, p1: Point, p2: Point) -> float:
    """Method to calculate the perpendicular distance between one point
    and a segment defined by two points"""

    # Identical line start and end points
    if p1.x == p2.x and p1.y == p2.y:
        return pointDistance(point, p1)

    # Quick fix for "vertical" lines
    slope = np.Infinity
    if p1.x != p2.x:
        slope = (p2.y - p1.y) / (p2.x - p1.x)

    b = -1
    c = -(slope * p1.x - p1.y)
    d = abs((slope * point.x + b * point.y + c)) / (math.sqrt(slope * slope + b * b))
    # print("Perpendicular distance is ", d)
    return d


def pointDistance(p0: Point, p1: Point) -> float:
    """Calculate euclidean distance between two given points"""

    dist = math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)
    return dist
