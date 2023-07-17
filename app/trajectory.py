from app.point import Point


class Trajectory:
    # Initialization method of trajectory with an unique id
    def __init__(self, number: int, points: list[Point] = None):
        """Representing a trajectory

        Attributes:
            number: ID of the trajectory
            points: Optional list of points from wich new points of the
                    trajectory are derived with an updated trajectory number

        """
        self.number = number
        self.points = []
        if points is not None:
            for point in points:
                # The trajectory number of the point is updated
                self.addPoint(Point(point.x, point.y, point.timestamp, self.number))

    def __repr__(self) -> str:
        # Nice printing of trajectory
        resultString = "Trajectory with number: " + str(self.number) + " and points"
        for p in self.points:
            resultString += str(p) + " "
        return resultString

    def addPoint(self, p: Point) -> None:
        """Adds a point to the trajectory"""
        self.points.append(p)
