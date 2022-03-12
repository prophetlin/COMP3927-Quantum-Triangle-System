"""
Quantum Triangle System
-----------------------

Quantum Triangle System Theory is all the rage in the world of Physics
these days. The Theory states that all matter is probabilistic and that
it moves along straight lines through "Quantum Triangles".

More specifically, a Quantum Triangle System is defined by an equilateral
triangle on the plane and $n$ quark trajectories cutting through the triangle.
Each quark trajectory $T_i$ is defined by a starting points $s_i$, an end point
$e_i$ and a probability $p_i$. The starting and end points lie on different
sides of the triangle, and the quark moves from $s_i$ to $e_i$ along a straight
line.

When two quark trajectories $T_i$ and $T_j$ meet at a point, the probability of
creating an entanglement is $p_i p_j$. If the trajectories do not meet, no
entanglement is created.

The expected number of entanglements is therefore,
$E(T_1, ..., T_n) = sum_{i < j: T_i and T_j meet} p_i p_j$
Your Physicist friend is on the brink of making a huge break thought, but her
current algorithm for computing $E(T_1, ..., T_n)$ is too slow. Help your
friend become the next Nobel Laureate by implementing an O(n log n) time
algorithm for computing $E(T_1, ..., T_n)$.

Assumption about the instance:
- assume all starting and end points are distinct
- assume the starting and end points are represented by a tuple (s, alpha)
  where s is in {0, 1, 2} specifies the side of the triangle (in clockwise
  order) and alpha in (0, 1) specifies how far along the side the point is
  (also in clockwise order)

"""

from collections import defaultdict
from quark_trajectories import QuarkTrajectory
from itertools import combinations

class QuantumTriangleSystem:
    """
    Quantum Triangles
    The system to detect the expected number of entanglements from the
    given quark trajectories.
    """

    sides = [0, 1, 2]

    def __init__(self, trajectories: list):
        """
        Initialise trajectories
        :param trajectories: List of trajectories
        """

        self.trajectories = trajectories.copy()

    def expected_entanglements_on_side_quadratic(self, side):
        """
        calculated expected entalgelments of trajectories that start or end on side
        """

        # swap start and end and reorient trajectories so that they start on side
        pivot = []
        for traj in self.trajectories:
            if traj.start.s == side:
                pivot.append(
                    QuarkTrajectory(traj.start, traj.end, traj.probability)
                )
            elif traj.end.s == side:
                pivot.append(
                    QuarkTrajectory(traj.end, traj.start, traj.probability)
                )
            else:
                # ignore this traj
                pass

        pivot.sort(key=lambda x: x.start.alpha)

        expected = 0.0

        for first, second in combinations(pivot, 2):

            # double check that first starts before second on side
            assert first.start.alpha < second.start.alpha, "first after second"
            assert first.start.s == side, "first not on side"
            assert second.start.s == side, "second not on side"

            next_side = (side + 1) % 3
            prev_side = (side + 2) % 3

            # if first -> next and second -> prev, count it fully
            if first.end.s == next_side and second.end.s == prev_side:
                expected += first.probability * second.probability
            # if first < second on the same side, count 0.5 (avoid double counting)
            elif first.end.s == second.end.s and first.end.alpha < second.end.alpha:
                expected += first.probability * second.probability / 2

        return expected


    def calculate_expected_entanglements_quadratic(self) -> float:
        """
        Calculates the expected entanglements in the list of trajectories.
        Runs in O(n^2) time.

        :return: The expected number of entanglements.
        """

        expected = 0.0

        for side in QuantumTriangleSystem.sides:
            expected += self.expected_entanglements_on_side_quadratic(side)

        return expected


    def merge_and_count(self, trajectories):
        """
        :param trajectories: pivoted trajectories
        :return: Sorted trajectories and expected number of entanglements
        """

        n = len(trajectories)

        expected = 0.0
        sorted_trajectories = []

        if n <= 1:
            sorted_trajectories = trajectories
        else:
            side = trajectories[0].start.s
            next_side = (side + 1) % 3
            prev_side = (side + 2) % 3

            # split trajectories into left and right
            mid = n // 2
            left, expected_left = self.merge_and_count(trajectories[:mid])
            right, expected_right = self.merge_and_count(trajectories[mid:])

            # compute forward sum of probabilities for next and prev side endpoint
            prob_next_side = 0.0
            prob_prev_side = 0.0
            for traj in right:
                if traj.end.s == next_side:
                    prob_next_side += traj.probability
                elif traj.end.s == prev_side:
                    prob_prev_side += traj.probability
                else:
                    raise ValueError("traj ends should be next of prev side")

            fwd_sum_next_side = [prob_next_side]
            fwd_sum_prev_side = [prob_prev_side]
            for traj in right:
                if traj.end.s == next_side:
                    prob_next_side -=  traj.probability
                elif traj.end.s == prev_side:
                    prob_prev_side -=  traj.probability

                fwd_sum_next_side.append(prob_next_side)
                fwd_sum_prev_side.append(prob_prev_side)

            expected = expected_left + expected_right

            # merge left and right
            left_index = 0
            right_index = 0
            while (left_index < len(left)) and (right_index < len(right)):
                left_end = left[left_index].end
                right_end = right[right_index].end
                # if left end comes before right_end
                if (
                    (left_end.s == next_side and right_end.s == prev_side) or
                    (left_end.s == right_end.s and left_end.alpha < right_end.alpha)
                    ):
                    left_traj = left[left_index]
                    sorted_trajectories.append(left_traj)
                    left_index += 1

                    # compute entanglement of left_traj and right[right_index:]
                    delta = left_traj.probability
                    if left_traj.end.s == next_side:
                        delta *= (fwd_sum_next_side[right_index] * 0.5 + 
                                fwd_sum_prev_side[right_index])
                    elif  left_traj.end.s == prev_side:
                        delta *= (fwd_sum_next_side[right_index] + 
                                fwd_sum_prev_side[right_index] * 0.5)
                    else:
                        raise ValueError("left_traj has two endpoints on side")
                    
                    expected += delta

                else:
                    sorted_trajectories.append(right[right_index])
                    right_index += 1

            # either left or right is finished, so let's finish the other one
            while (left_index + right_index < n):
                # if we are done with the left
                if left_index == len(left):
                    sorted_trajectories.append(right[right_index])
                    right_index += 1
                # if we are done with the right  
                elif right_index == len(right):
                    sorted_trajectories.append(left[left_index])
                    left_index += 1
                # if not is done something went wrong
                else:
                    raise ValueError("Bug in the previous while loop")
        
        return (sorted_trajectories, expected)


    def expected_entanglements_on_side(self, side):
        """
        calculated expected entalgelments of trajectories that start or end on side
        """


        # swap start and end and reorient trajectories so that they start on side
        pivot = []
        for traj in self.trajectories:
            if traj.start.s == side:
                pivot.append(
                    QuarkTrajectory(traj.start, traj.end, traj.probability)
                )
            elif traj.end.s == side:
                pivot.append(
                    QuarkTrajectory(traj.end, traj.start, traj.probability)
                )
            else:
                # ignore this traj
                pass

        pivot.sort(key=lambda x: x.start.alpha)

        return self.merge_and_count(pivot)[-1]

    def calculate_expected_entanglements(self) -> float:
        """
        Calculates the expected entanglements in the list of trajectories.
        Must run in O(n log n) time, or else it will be too slow for your
        friend!

        :return: The expected number of entanglements.
        """

        expected = 0.0

        for side in QuantumTriangleSystem.sides:
            expected += self.expected_entanglements_on_side(side)

        return expected
