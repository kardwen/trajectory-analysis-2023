from app.point import Point
from app.r_tree import MBR


class Region:
    # Initialization method of region
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center
        self.radius = radius

    # Checks if point lies in region
    def pointInRegion(self, queryPoint: Point) -> bool:
        # Pythagoras
        squaredDistSum = (queryPoint.x - self.center.x) ** 2 + (queryPoint.y - self.center.y) ** 2
        return squaredDistSum <= self.radius**2

    def intersectsMBR(self, mbr: MBR) -> bool:
        # Calculate the minimum distance from the region's center to the MBR in x and y direction
        # For each direction exist three different cases
        dx = max((mbr.minX - self.center.x), (self.center.x - mbr.maxX), 0)
        dy = max((mbr.minY - self.center.y), (self.center.y - mbr.maxY), 0)
        squaredDistSum = dx**2 + dy**2

        # Check if the squared distance is less than or equal to the squared radius
        return squaredDistSum <= self.radius**2
