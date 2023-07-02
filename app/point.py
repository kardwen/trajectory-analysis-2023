class Point:
    # Initialization method of point with two coordinates x and y
    def __init__(self, x: float, y: float, timestamp):
        self.x = x
        self.y = y
        self.timestamp = timestamp

    # Nice printing of point
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.timestamp) + ")"

    # Test for equality of points
    def __eq__(self, other):
        if isinstance(other, Point):
            return (
                self.x == other.x
                and self.y == other.y
                and self.timestamp == other.timestamp
            )
        return False
