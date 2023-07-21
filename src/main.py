from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from app import utils

# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))
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
