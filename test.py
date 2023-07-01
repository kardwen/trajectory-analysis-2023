import unittest

from app import functions_template as functions
from app.point import Point
from app.trajectory import Trajectory


class TestDouglasPeucker(unittest.TestCase):
    def testMinimalTrajectory(self):
        """
        Test that it can handle a trajectory only containing two points
        """
        result = functions.douglasPeucker(
            Trajectory(
                0,
                [
                    Point(0.1, 0.2, "2000-01-01 01:18:21"),
                    Point(0.3, 0.4, "2000-01-01 01:18:22"),
                ],
            ),
            1.0,
        )
        self.assertEqual(len(result.points), 2)
        self.assertEqual(result.points[0], Point(0.1, 0.2, "2000-01-01 01:18:21"))
        self.assertEqual(result.points[1], Point(0.3, 0.4, "2000-01-01 01:18:22"))

    def testEmptyTrajectory(self):
        """
        Test that it can handle an empty trajectory
        """
        result = functions.douglasPeucker(
            Trajectory(0),
            1.0,
        )
        self.assertEqual(len(result.points), 0)

    def testTrajectoryWithCollinearPoints(self):
        """
        Test that it can handle a trajectory with collinear points
        """
        result = functions.douglasPeucker(
            Trajectory(
                0,
                [
                    Point(0.1, 0.2, "2000-01-01 01:18:21"),
                    Point(0.3, 0.4, "2000-01-01 01:18:22"),
                    Point(0.5, 0.6, "2000-01-01 01:18:23"),
                    Point(0.7, 0.8, "2000-01-01 01:18:24"),
                    Point(0.9, 1.0, "2000-01-01 01:18:25"),
                ],
            ),
            0.1,
        )
        # The result should only contain the first and last point
        self.assertEqual(len(result.points), 2)
        self.assertEqual(result.points[0], Point(0.1, 0.2, "2000-01-01 01:18:21"))
        self.assertEqual(result.points[1], Point(0.9, 1.0, "2000-01-01 01:18:25"))

    def testTrajectoryWithCurvatureLargeEpsilon(self):
        """
        Test that it can handle a trajectory with curvature and large epsilon
        """
        result = functions.douglasPeucker(
            Trajectory(
                0,
                [
                    Point(0.1, 0.2, "2000-01-01 01:18:21"),
                    Point(0.5, 0.7, "2000-01-01 01:18:22"),
                    Point(0.8, 0.5, "2000-01-01 01:18:23"),
                    Point(1.0, 0.3, "2000-01-01 01:18:24"),
                ],
            ),
            1.0,
        )
        # The result should contain the start and end point
        # because the distance to a straight line is alway smaller than epsilon
        self.assertEqual(len(result.points), 2)
        self.assertEqual(result.points[0], Point(0.1, 0.2, "2000-01-01 01:18:21"))
        self.assertEqual(result.points[1], Point(1.0, 0.3, "2000-01-01 01:18:24"))

    def testTrajectoryWithCurvatureSmallEpsilon(self):
        """
        Test that it can handle a trajectory with curvature and small epsilon
        """
        result = functions.douglasPeucker(
            Trajectory(
                0,
                [
                    Point(0.1, 0.2, "2000-01-01 01:18:21"),
                    Point(0.5, 0.7, "2000-01-01 01:18:22"),
                    Point(0.8, 0.5, "2000-01-01 01:18:23"),
                    Point(1.0, 0.3, "2000-01-01 01:18:24"),
                ],
            ),
            0.1,
        )
        # The result should contain the start and end point and one additional
        # point in between because of the value of epsilon
        self.assertEqual(len(result.points), 3)
        self.assertEqual(result.points[0], Point(0.1, 0.2, "2000-01-01 01:18:21"))
        self.assertEqual(result.points[1], Point(0.5, 0.7, "2000-01-01 01:18:22"))
        self.assertEqual(result.points[2], Point(1.0, 0.3, "2000-01-01 01:18:24"))


if __name__ == "__main__":
    unittest.main()
