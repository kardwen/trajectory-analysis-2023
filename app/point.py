class point:
    # Initialization method of point with two coordinates x and y
    def __init__(self, x: float, y: float, timestamp):
        self.X = x
        self.Y = y
        self.timestamp = timestamp

    # Nice printing of point
    def __str__(self) -> str:
        return "(" + str(self.X) + "," + str(self.Y) + "," + str(self.timestamp) + ")"
