from pathlib import Path
from app import functions
from app import utils


# Import trajectories
trajectoriesDir = Path.cwd() / "data" / "trajectories"
listOfTrajectories = utils.importTrajectories(str(trajectoriesDir))


# Calculate the distance between at least two trajectories with
# Closest-Pair-Distance and Dynamic Time Warping

# Closest-Pair-Distance
closestPairDist = functions.closestPairDistance(
    listOfTrajectories[4], listOfTrajectories[5]
)
print(
    f"The closest-pair distance between Trajectory #{listOfTrajectories[4].number}",
    f"and Trajectory #{listOfTrajectories[5].number} is {closestPairDist}.",
)

# Dynamic Time Warping
# TODO
