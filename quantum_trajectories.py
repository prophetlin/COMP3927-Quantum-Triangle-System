"""
Quark Trajectories

A trajectory of quarks, has a start and end point.
Is used in the Quantum Triangles System to detect
if any of the quark trajectories are entangled.
"""


class Position:
    """
    Position for starting and ending the trajectory
    """
    def __init__(self, s: int, alpha: float):
        """
        Initialise the position
        :param s: The side of the triangle, where s in [0, 1, 2]
        :param alpha: How far along the side of the triangle. Must be in (0, 1)
        """
        self.s = s
        self.alpha = alpha

    def __repr__(self):

        return "({}, {})".format(self.s, self.alpha)

class QuarkTrajectory:
    """
    Trajectory of quarks
    """
    def __init__(self, start: Position, end: Position, probability: float):
        """
        Initialise the trajectory with start, end and probability.
        :param start: The starting point of the trajectory.
        :param end: The end point of the trajectory.
        :param probability: The probability of this trajectory forming an
                            entanglement.
        """
        self.start = start
        self.end = end
        self.probability = probability

    def __repr__(self):

        return "QuarkTrajectory({}, {}, {})".format(self.start, self.end, self.probability)
