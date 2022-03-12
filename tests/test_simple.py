import math
import random
import unittest

import timeout_decorator

from quantum_traingles import QuantumTriangleSystem
from quark_trajectories import Position, QuarkTrajectory

###################
# Helper Functions
###################


def assert_equal(got, expected, msg):
    """
    Simple asset helper
    """
    assert expected == got, \
        "[{}] Expected: {}, got: {}".format(msg, expected, got)


def assert_is_close(got, expected, msg, err=0.001):
    """
    Simple asset helper
    """
    assert abs(expected - got) < err, \
        "[{}] Expected: {}, got: {}".format(msg, expected, got)


class SimpleTestCase(unittest.TestCase):

    def new_position(self, side: int, i: int, n: int) -> Position:
        """
        Create a new position (i + 1) / (n + 1) along the way on side
        :param side: Side of the quantum triangle
        :param i: index in [0:n]
        :param n: total number of points.
        :return: Position
        """

        return Position(side, (i + 1) / (n + 1))

    def all_positions(self, n: int) -> dict:
        """
        Create a n positions on each side
        :param n: total number of points on one side.
        :return: dict mapping (s, i) to Position
        """

        ans = dict()

        for side in QuantumTriangleSystem.sides:
            for i in range(n):
                ans[side, i] = self.new_position(side, i, n)

        return ans

    def test_same_single_cross(self):
        """ #score(1) """

        start_i = Position(0, 0.3)
        start_j = Position(0, 0.5)
        end_i = Position(1, 0.8)
        end_j = Position(1, 0.85)

        trajectories = [
            QuarkTrajectory(start_i, end_i, 0.5),
            QuarkTrajectory(start_j, end_j, 0.5)
        ]

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            (0.5 * 0.5),
            "Expected entanglements for one overlap with len(trajectories) = 2"
        )

    def test_same_side_no_cross(self):
        """ #score(1) """

        start_i = Position(0, 0.3)
        start_j = Position(0, 0.5)
        end_j = Position(1, 0.8)
        end_i = Position(1, 0.85)

        trajectories = [
            QuarkTrajectory(start_i, end_i, 0.5),
            QuarkTrajectory(start_j, end_j, 0.5)
        ]

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "Expected entanglements for 0 overlap with len(trajectories) = 2"
        )

    def test_three_trajectories_cross(self):
        """ #score(2) """

        n = 2
        pos = self.all_positions(n)

        trajectories = []

        for side in QuantumTriangleSystem.sides:
            next_side = (side + 1) % 3

            trajectories.append(
                QuarkTrajectory(pos[side, 0], pos[next_side, 1], 0.5)
            )

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            3/4,
            "expected entanglements for all cross n=2"
        )

    def test_simple_none_touch(self):
        """ #score(1) """

        n = 2
        pos = self.all_positions(n)

        trajectories = []

        for side in QuantumTriangleSystem.sides:
            next_side = (side + 1) % 3

            trajectories.append(
                QuarkTrajectory(pos[side, 1], pos[next_side, 0], 0.5)
            )

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "expected entanglements for all cross n=2"
        )

    def test_simple_no_trajectories(self):
        """ #score(1) """

        trajectories = []

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "expected 0 entanglements for no trajectories"
        )

    @timeout_decorator.timeout(1)
    def test_two_sided_large_nonuniform_efficiency(self):
        """ #score(3) """

        n = 10000

        pos = self.all_positions(n)

        trajectories = []

        sum_p = 0.0
        sum_p_square = 0.0

        for i in range(n):
            p = random.random()
            sum_p += p
            sum_p_square += p ** 2

            trajectories.append(
                QuarkTrajectory(pos[0, i], pos[1, i], p)
            )

        qs = QuantumTriangleSystem(trajectories)
        expected = (sum_p ** 2 - sum_p_square) / 2

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "expected entanglements"
        )

    @timeout_decorator.timeout(1)
    def test_two_sided_large_nonuniform(self):
        """ #score(2) """

        n = 1000

        pos = self.all_positions(n)

        trajectories = []

        sum_p = 0.0
        sum_p_square = 0.0

        for i in range(n):
            p = random.random()
            sum_p += p
            sum_p_square += p ** 2

            trajectories.append(
                QuarkTrajectory(pos[0, i], pos[1, i], p)
            )

        qs = QuantumTriangleSystem(trajectories)
        expected = (sum_p ** 2 - sum_p_square) / 2

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "expected entanglements"
        )

    def test_small_recursive_triforce(self):
        """ #score(1) """

        alphas = [0.1, 0.2, 0.3, 0.4, 0.49, 0.51, 0.6, 0.7, 0.8, 0.9]

        trajectories = []
        for side in QuantumTriangleSystem.sides:
            for i in range(5, len(alphas)):
                trajectories.append(
                    QuarkTrajectory(
                        Position(side, alphas[i]),
                        Position((side+1) % 3, alphas[-i-1]),
                        1
                    )
                )

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "Expected 0 entanglements for non intersecting trajectories"
        )

    @timeout_decorator.timeout(1)
    def test_large_recursive_triforce(self):
        """ #score(2) #hidden """

        alphas = [(x * 0.001) for x in range(1, 1000)]

        trajectories = []
        for side in QuantumTriangleSystem.sides:
            for i in range(math.floor(len(alphas) / 2) + 1, len(alphas)):
                trajectories.append(
                    QuarkTrajectory(
                        Position(side, alphas[i]),
                        Position((side + 1) % 3, alphas[-i - 1]),
                        1
                    )
                )

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "Expected 0.0 for non intersecting trajectories"
        )

    @timeout_decorator.timeout(1)
    def test_large_recursive_triforce_efficiency(self):
        """ #score(2) #hidden """

        alphas = [(x * 0.0001) for x in range(1, 10000)]

        trajectories = []
        for side in QuantumTriangleSystem.sides:
            for i in range(math.floor(len(alphas) / 2) + 1, len(alphas)):
                trajectories.append(
                    QuarkTrajectory(
                        Position(side, alphas[i]),
                        Position((side + 1) % 3, alphas[-i - 1]),
                        1
                    )
                )

        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "Expected 0.0 for non intersecting trajectories"
        )


    @timeout_decorator.timeout(1)
    def test_single_filled_side_no_overlap(self):
        """ #score(1) """

        trajectories = []

        for i in range(0, 10000):
            trajectories.append(
                QuarkTrajectory(
                    Position(1, 0.0001*i),
                    Position(2, 0.9-(0.0001 * i)),
                    0.95
                )
            )


        qs = QuantumTriangleSystem(trajectories)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            0.0,
            "Expected 0 for non-intersecting trajectories."
        )


    def test_dark_side_of_the_moon(self):
        """ #score(2) """

        trajectories = []

        # Bottom
        for i in range(1, 9):
            trajectories.append(
                QuarkTrajectory(
                    Position(0, 0.1 * i),
                    Position(1, 0.95 - (0.1 * i)),
                    1
                )
            )

        for i in range(1, 9):
            trajectories.append(
                QuarkTrajectory(
                    Position(1, 0.1 * i),
                    Position(2, 0.9 - (0.1 * i)),
                    1
                )
            )

        qs = QuantumTriangleSystem(trajectories)

        expected = ((8 * (1 + 8)) / 2)

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "Entangled trajectories"
        )

    @timeout_decorator.timeout(1)
    def test_large_n_overlap(self):
        """ #score(2) """

        n = 2000

        pos = self.all_positions(n)

        trajectories = []

        sum_p = 0.0
        sum_p_square = 0.0

        for i in range(n):

            p = random.randrange(0, 100) / 100
            sum_p += p

            sum_p_square += p ** 2

            trajectories.append(
                QuarkTrajectory(pos[0, i], pos[2, i], p)
            )

        qs = QuantumTriangleSystem(trajectories)

        expected = (sum_p**2 - sum_p_square) / 2

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "Expected entanglements for n=2000"
        )

    @timeout_decorator.timeout(1)
    def test_large_n_overlap_efficiency(self):
        """ #score(5) """

        n = 10000

        pos = self.all_positions(n)

        trajectories = []

        sum_p = 0.0
        sum_p_square = 0.0

        for i in range(n):

            p = random.randrange(0, 100) / 100
            sum_p += p

            sum_p_square += p ** 2

            trajectories.append(
                QuarkTrajectory(pos[0, i], pos[2, i], p)
            )

        qs = QuantumTriangleSystem(trajectories)

        expected = (sum_p**2 - sum_p_square) / 2

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "Expected entanglements for n=2000"
        )


    @timeout_decorator.timeout(1)
    def test_three_side_large(self):
        """ #score(2) get cor """

        starts = [x * 0.001 for x in range(2, 1000, 2)]
        ends = [x * 0.001 for x in range(3, 1000, 2)]

        trajectories = []

        for side in QuantumTriangleSystem.sides:
            for i in range(0, len(starts)):
                trajectories.append(
                    QuarkTrajectory(
                        Position(side, starts[i]),
                        Position((side + 1) % 3, ends[i]),
                        0.9
                    )

                )


        qs = QuantumTriangleSystem(trajectories)
        # expected = (3 * (499 * (499 + 1) / 2))
        expected = 605072.43

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "Expected entanglements"
        )

    @timeout_decorator.timeout(1)
    def test_three_side_large_efficiency(self):
        """ #score(6) #hidden """

        starts = [x * 0.0001 for x in range(2, 10000, 2)]
        ends = [x * 0.0001 for x in range(3, 10000, 2)]

        trajectories = []

        for side in QuantumTriangleSystem.sides:
            for i in range(0, len(starts)):
                trajectories.append(
                    QuarkTrajectory(
                        Position(side, starts[i]),
                        Position((side + 1) % 3, ends[i]),
                        0.9
                    )

                )


        qs = QuantumTriangleSystem(trajectories)
        # expected = (3 * (4999 * 4999)) * 0.9 * 0.9
        expected = 60725702.43

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "Expceted entanglements"
        )


    def test_twoside_overlaps(self):
        """ #score(2) #hidden """

        starts = [x * 0.1 for x in range(1, 10)]
        ends = [0.05 + (x * 0.1) for x in range(1, 10)]


        trajectories = []

        # Side 1
        for i in range(0, len(starts)):
            trajectories.append(
                QuarkTrajectory(
                    Position(1, starts[i]),
                    Position(2, ends[-(1 + i)]),
                    0.8
                )
            )

        # Side 2
        for i in range(0, len(starts)):
            trajectories.append(
                QuarkTrajectory(
                    Position(2, starts[i]),
                    Position(0, ends[-(1 + i)]),
                    0.7
                )
            )


        qs = QuantumTriangleSystem(trajectories)

        expected = 25.2

        assert_is_close(
            qs.calculate_expected_entanglements(),
            expected,
            "Expected entanglements"
        )


