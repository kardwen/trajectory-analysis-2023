from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from app.point import Point
from app.region import Region
from app import utils
import app.functions_template as functions


# Import trajectories
trajectories_dir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectories_dir))
# print(listOfTrajectories)


# Visualize trajectories
colorMap = matplotlib.colormaps["viridis"]
colors = [*map(colorMap, np.linspace(0, 1, len(listOfTrajectories)))]

figure = plt.figure()

for i, origTrajectory in enumerate(listOfTrajectories):
    x = [point.x for point in origTrajectory.points]
    y = [point.y for point in origTrajectory.points]
    plt.plot(
        x,
        y,
        color=colors[i],
        label=f"Trajectory {origTrajectory.number}",
    )

plt.title("2D Trajectories")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis("equal")
figure.tight_layout()
plt.show(block=True)


# Simplify at least one of the trajectories with Douglas Peucker
# and/or Sliding Window Algorithm
origTrajectory = listOfTrajectories[40]
print(f"Original trajectory #{origTrajectory.number}, point count: {len(origTrajectory.points)}")
simplifiedTrajectory1 = functions.douglasPeucker(origTrajectory, 0.00001)
print(f"Simplified trajectory (epsilon={0.00001}), point count: {len(simplifiedTrajectory1.points)}")
simplifiedTrajectory2 = functions.douglasPeucker(origTrajectory, 0.0002)
print(f"Simplified trajectory (epsilon={0.0002}), point count: {len(simplifiedTrajectory2.points)}")

# Visualize original trajectory and its two simplifications
colorMap = matplotlib.colormaps["viridis"]
colors = [*map(colorMap, np.linspace(0, 1, 3))]

figure = plt.figure()

x = [point.x for point in origTrajectory.points]
y = [point.y for point in origTrajectory.points]
plt.plot(
    x,
    y,
    color=colors[0],
    label=f"Trajectory #{origTrajectory.number}",
)
x = [point.x for point in simplifiedTrajectory1.points]
y = [point.y for point in simplifiedTrajectory1.points]
plt.plot(
    x,
    y,
    color=colors[1],
    label=f"Trajectory #{simplifiedTrajectory1.number}, e={0.00001}",
)
x = [point.x for point in simplifiedTrajectory2.points]
y = [point.y for point in simplifiedTrajectory2.points]
plt.plot(
    x,
    y,
    color=colors[2],
    label=f"Trajectory #{str(simplifiedTrajectory2.number)}, e={0.0002}",
)

plt.title("Simplified Trajectories - Douglas Peucker algorithm")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.axis("equal")
figure.tight_layout()
plt.show(block=True)


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
