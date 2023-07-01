from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from point import Point
from region import Region
import utils
import functions_template as functions

# Import trajectories
trajectories_dir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectories_dir))
# print(listOfTrajectories)

# Visualize trajectories
colorMap = matplotlib.colormaps["viridis"]
colors = [*map(colorMap, np.linspace(0, 1, len(listOfTrajectories)))]
for i, trajectory in enumerate(listOfTrajectories):
    x = [point.x for point in trajectory.points]
    y = [point.y for point in trajectory.points]
    plt.plot(
        x,
        y,
        color=colors[i],
        label=f"Trajectory {str(trajectory.number)}",
    )

plt.title("2D Trajectories")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

# Simplify at least one of the trajectories with Douglas Peucker
# and/or Sliding Window Algorithm

# Visualize original trajectory and its two simplifications

# Calculate the distance between at least two trajectories with
# Closest-Pair-Distance and/or Dynamic Time Warping

# Build R-tree with all given 62 trajectories

# Query the trajectories using the built R-tree and the region.
# Which trajectories lie in the given region?
# This query should return the trajectories with ids 43, 45, 50, 71, 83
queryRegion = Region(Point(0.0012601754558545508, 0.0027251228043638775, 0.0), 0.00003)
foundTrajectories = functions.solveQueryWithRTree(queryRegion, listOfTrajectories)
if foundTrajectories is not None:
    if len(foundTrajectories) == 0:
        print("No trajectories match the query.")
    for t in foundTrajectories:
        print(t)
