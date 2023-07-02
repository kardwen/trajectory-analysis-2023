from app.point import Point


class Trajectory:
    # Initialization method of trajectory with an unique id
    def __init__(self, number: int, points: list[Point] = None):
        self.number = number
        self.points = []
        if points is not None:
            for point in points:
                self.addPoint(point)

    def __repr__(self) -> str:
        # Nice printing of trajectory
        resultString = "Trajectory with number: " + str(self.number) + " and points"
        for p in self.points:
            resultString += str(p) + " "
        return resultString

    # Adds a point to the list of points of the trajectory
    def addPoint(self, p: Point) -> None:
        self.points.append(p)
