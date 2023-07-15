from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from app import functions
from app.trajectory import Trajectory
from app.point import Point
from app.region import Region
from app import utils


# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))
# print(listOfTrajectories)


# Visualize trajectories
colorMap = matplotlib.colormaps["viridis"]
colors = [*map(colorMap, np.linspace(0, 1, 2))]

testTrajectory1 = Trajectory(
    0,
    [
        Point(0.1, 0.2, "2000-01-01 01:18:21"),
        Point(0.5, 0.7, "2000-01-01 01:18:22"),
        Point(0.8, 0.5, "2000-01-01 01:18:23"),
    ],
)
testTrajectory2 = Trajectory(
    1,
    [
        Point(0.1, -0.2, "2000-01-01 01:18:21"),
        Point(0.5, 0.6, "2000-01-01 01:18:22"),
        Point(0.8, -0.2, "2000-01-01 01:18:23"),
    ],
)

figure = plt.figure()
x = [point.x for point in testTrajectory1.points]
y = [point.y for point in testTrajectory1.points]
plt.plot(
    x,
    y,
    color=colors[0],
    label=f"Trajectory #{testTrajectory1.number}",
)
x = [point.x for point in testTrajectory2.points]
y = [point.y for point in testTrajectory2.points]
plt.plot(
    x,
    y,
    color=colors[0],
    label=f"Trajectory #{testTrajectory2.number}",
)
plt.title("Test Trajectories")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.axis("equal")
figure.tight_layout()
plt.show(block=True)
