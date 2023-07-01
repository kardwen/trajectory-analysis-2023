from app.point import Point


class Region:
    # Initialization method of region
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center
        self.radius = radius

    # Checks if point lies in region
    def pointInRegion(self, queryPoint: Point) -> bool:
        # TODO
        return None
