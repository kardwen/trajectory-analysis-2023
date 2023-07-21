from pathlib import Path

from app import functions, utils
from app.point import Point
from app.r_tree import RTree
from app.region import Region

# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))


# Build R-tree with all given 62 trajectories
points = []
for trajectory in listOfTrajectories:
    points.extend(trajectory.points)

rTree = RTree(points)

# Query the trajectories using the built R-tree and the region.
# Which trajectories lie in the given region?
# This query should return the trajectories with ids 43, 45, 50, 71, 83
queryRegion = Region(Point(0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)

foundTrajectories = functions.solveQueryWithRTree(
    queryRegion, rTree, listOfTrajectories
)
if len(foundTrajectories) > 0:
    print(
        f"Found trajectories {[trajectory.number for trajectory in foundTrajectories]}",
        "within region (search in R-Tree)",
    )
else:
    print("No trajectories match the query.")

foundTrajectories = functions.solveQueryWithoutRTree(queryRegion, listOfTrajectories)
if len(foundTrajectories) > 0:
    print(
        f"Found trajectories {[trajectory.number for trajectory in foundTrajectories]}",
        "within region",
    )
else:
    print("No trajectories match the query.")
