import numpy as np
from pytest import approx

from app.functions import dynamicTimeWarping
from app.point import Point
from app.trajectory import Trajectory


def testEmptyTrajectories():
    """
    Tests that it can handle invalid trajectories without points
    """
    result = dynamicTimeWarping(Trajectory(0), Trajectory(1))
    assert result == np.Infinity


def testEqualTrajectories():
    """
    Tests equal trajectories
    """
    result = dynamicTimeWarping(
        Trajectory(
            0,
            [
                Point(1.0, 0.2, "2000-01-01 01:18:21"),
                Point(2.0, 0.7, "2000-01-01 01:18:22"),
                Point(3.0, 0.5, "2000-01-01 01:18:23"),
                Point(3.0, 0.1, "2000-01-01 01:18:23"),
            ],
        ),
        Trajectory(
            1,
            [
                Point(1.0, 0.2, "2000-01-01 01:18:21"),
                Point(2.0, 0.7, "2000-01-01 01:18:22"),
                Point(3.0, 0.5, "2000-01-01 01:18:23"),
                Point(3.0, 0.1, "2000-01-01 01:18:23"),
            ],
        ),
    )
    assert result == 0.0


def testMinimalTrajectories():
    """
    Tests that it can handle trajectories only containing two points
    """
    result = dynamicTimeWarping(
        Trajectory(
            0,
            [
                Point(0.1, 0.8, "2000-01-01 01:18:21"),
                Point(0.2, 1.2, "2000-01-01 01:18:22"),
            ],
        ),
        Trajectory(
            1,
            [
                Point(0.1, 1.2, "2000-01-01 01:18:21"),
                Point(0.2, 1.4, "2000-01-01 01:18:22"),
            ],
        ),
    )
    assert result == approx(0.2)


def testTrajectories():
    """
    Tests two trajectories with different lengths and curvature
    """
    result = dynamicTimeWarping(
        Trajectory(
            0,
            [
                Point(0.1, 0.2, "2000-01-01 01:18:21"),
                Point(0.5, 0.7, "2000-01-01 01:18:22"),
                Point(0.8, 0.5, "2000-01-01 01:18:23"),
            ],
        ),
        Trajectory(
            1,
            [
                Point(0.1, -0.2, "2000-01-01 01:18:21"),
                Point(0.3, 0.1, "2000-01-01 01:18:22"),
                Point(0.5, 0.4, "2000-01-01 01:18:23"),
                Point(0.8, -0.2, "2000-01-01 01:18:24"),
            ],
        ),
    )
    assert result == approx(0.3166667, rel=1e-4)


def testParallelTrajectories():
    """
    Tests DTW distance of parallel trajectories
    """
    result = dynamicTimeWarping(
        Trajectory(
            0,
            [
                Point(0.1, 1.2, "2000-01-01 01:18:21"),
                Point(0.5, 1.2, "2000-01-01 01:18:22"),
                Point(0.8, 1.2, "2000-01-01 01:18:23"),
                Point(1.1, 1.2, "2000-01-01 01:18:24"),
            ],
        ),
        Trajectory(
            1,
            [
                Point(0.1, 2.2, "2000-01-01 01:18:21"),
                Point(0.5, 2.2, "2000-01-01 01:18:22"),
                Point(0.8, 2.2, "2000-01-01 01:18:23"),
                Point(1.1, 2.2, "2000-01-01 01:18:24"),
            ],
        ),
    )
    assert result == approx(1.0)
