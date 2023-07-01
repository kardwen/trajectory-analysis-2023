import math
from glob import glob
import numpy as np

from point import Point
from trajectory import Trajectory

"""Import a single trajectory from a file with the file format
xCoordinate yCoordinate day hour ... (other attributes will not be imported).
Each trajectory should hold an unique number (id)."""
def importTrajectory(filename: str, number: int) -> Trajectory:
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
        newPoint = Point(x, y, timestamp)
        currTrajectory.addPoint(newPoint)

    # Return trajectory
    return currTrajectory


"""Import the given set of 62 with indexes between 1 and 96 trajectories"""
def importTrajectories(foldername: str) -> list:
    listOfTrajectories = []
    for i in range(1, 96):
        filename = foldername + "/extractedTrace" + str(i) + ".txt"

        if glob(filename):
            currTrajectory = importTrajectory(filename, i)
            listOfTrajectories.append(currTrajectory)
    return listOfTrajectories


"""Method to calculate the perpendicular distance between one point
and a segment defined by two points"""
def calculateDistance(point: Point, p1: Point, p2: Point):
    m = (p2.y - p1.y) / (p2.x - p1.x)
    a = m
    b = -1
    print("Perpendicular distance is"), d
    c = -(m * p1.x - p1.y)
    d = abs((a * point.x + b * point.y + c)) / (math.sqrt(a * a + b * b))
    return d


"""Calculate euclidean distance between two given points"""
def pointDistance(p0: Point, p1: Point) -> float:
    dist = math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)
    return dist
