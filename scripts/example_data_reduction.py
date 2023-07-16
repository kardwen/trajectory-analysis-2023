from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from app import functions
from app import utils


# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))


# Simplify at least one of the trajectories with Douglas Peucker
# and/or Sliding Window Algorithm
origTrajectory = listOfTrajectories[40]
print(
    f"Original trajectory #{origTrajectory.number}, point count: {len(origTrajectory.points)}"
)
simplifiedTrajectory1 = functions.douglasPeucker(origTrajectory, 0.00001)
print(
    f"Simplified trajectory - Douglas Peucker (epsilon={0.00001}), point count: {len(simplifiedTrajectory1.points)}"
)
simplifiedTrajectory2 = functions.douglasPeucker(origTrajectory, 0.0002)
print(
    f"Simplified trajectory - Douglas Peucker (epsilon={0.0002}), point count: {len(simplifiedTrajectory2.points)}"
)

# Visualize original trajectory and its two simplifications
colorMap = matplotlib.colormaps["viridis"]
colors = [*map(colorMap, np.linspace(0, 1, 3))]

figure = plt.figure()

plt.plot(
    [point.x for point in origTrajectory.points],
    [point.y for point in origTrajectory.points],
    color=colors[0],
    label=f"Trajectory #{origTrajectory.number}",
)
plt.plot(
    [point.x for point in simplifiedTrajectory1.points],
    [point.y for point in simplifiedTrajectory1.points],
    color=colors[1],
    label=f"Trajectory #{simplifiedTrajectory1.number}, e={0.00001}",
)
plt.plot(
    [point.x for point in simplifiedTrajectory2.points],
    [point.y for point in simplifiedTrajectory2.points],
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
# plt.show(block=True)


# Sliding window algorithm
print(
    f"Original trajectory #{origTrajectory.number}, point count: {len(origTrajectory.points)}"
)
simplifiedTrajectory1 = functions.slidingWindow(origTrajectory, 0.00001)
print(
    f"Simplified trajectory - Sliding window (epsilon={0.00001}), point count: {len(simplifiedTrajectory1.points)}"
)
simplifiedTrajectory2 = functions.slidingWindow(origTrajectory, 0.0002)
print(
    f"Simplified trajectory - Sliding window (epsilon={0.0002}), point count: {len(simplifiedTrajectory2.points)}"
)

# Visualize original trajectory and its two simplifications
colorMap = matplotlib.colormaps["viridis"]
colors = [*map(colorMap, np.linspace(0, 1, 3))]

figure = plt.figure()

plt.plot(
    [point.x for point in origTrajectory.points],
    [point.y for point in origTrajectory.points],
    color=colors[0],
    label=f"Trajectory #{origTrajectory.number}",
)
plt.plot(
    [point.x for point in simplifiedTrajectory1.points],
    [point.y for point in simplifiedTrajectory1.points],
    color=colors[1],
    label=f"Trajectory #{simplifiedTrajectory1.number}, e={0.00001}",
)
plt.plot(
    [point.x for point in simplifiedTrajectory2.points],
    [point.y for point in simplifiedTrajectory2.points],
    color=colors[2],
    label=f"Trajectory #{str(simplifiedTrajectory2.number)}, e={0.0002}",
)

plt.title("Simplified Trajectories - Sliding window algorithm")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.axis("equal")
figure.tight_layout()

plt.show(block=True)
