# Quantum Triangle System Theory

Here there be physics.

Here there be physics.
Assignment 6 - Quantum Triangle System

Story

Quantum Triangle System Theory is all the rage in the world of Physics these days. The theory says that all mater is probabilistic and that it moves along straight lines through Quantum Triangles.

More specifically, a Quantum Triangle System is defined by an equilateral triangle on the plane and n quark trajectories cutting through the triangle. Each quark trajectory T_i is defined by a starting points s_i, an end point e_i and a probability p_i. The starting and end points lie on different sides of the triangle, and the quark moves from s_i to e_i along a straight line.

When two quark trajectories T_i and T_j meet at a point, the probability of creating an entanglement is p_i p_j. If the trajectories do not meet, no entanglement is created.The expected number of entanglements is therefore: 

```
E(T_1, \ldots, T_n) = \sum_{i < j:\ T_i\ and\ T_j\ meet} p_i\ p_j
```

Your Physicist friend is on the brink of making a huge break thought, but her current algorithm for computing E(T_1, ..., T_n) is too slow. Help your friend become the next Nobel Laureate by implementing an O(n log n) time algorithm for computing E(T_1, ..., T_n).


## About the code

**quark_trajectories.py (does not require modification)**

Contains the classes that are related to the trajectories.

```
class Position
```

The position on the triangle, has two attributes: 

* `s` - the side of the triangle, where s in [0, 1, 2].

* `alpha` - the position along the side of the triangle, must be in (0, 1).

```
class QuarkTrajectory
```

The trajectory information, contains:

* `start` (type: Position) - the start position of the trajectory.
* `end` (type: Position) - the end position of the trajectory.
* `probability` (type float) - the probability of the trajectory forming an entanglement.


**quantum_triangles.py (implement your code here)**

```
class QuantumTriangle
```

Is the main triangle class, it is given a list of trajectories, and must calculate the expected entanglements.

**Properties:**

* trajectories (type: List[QuarkTrajectory]) - the list of trajectories in the quantum triangle system.

Functions:

* calculate_expected_entanglements(self) -> float 

Takes no arguments, and returns a float.

Calculates the entanglements from the list of trajectories stored in self.trajectories. 

Must be O(n log N) or your friend will be sad :(

Example:

If we had two trajectories t_1 and t_2. Defined as follows:

```
                               # pos start       # pos end        # probability
trajectory_1 (blue) = QuarkTrajectory(Position(0, 0.7), Position(2, 0.6), 0.8)
trajectory_2 (orange) = QuarkTrajectory(Position(1, 0.6), Position(2, 0.85), 0.9)

trajectories = [trajectory_1, trajectory_2]
quantum_system = QuantumTriangleSystem(trajectories)

quantum_system.calculate_expected_entanglements()
```

in this example would be be:
```
trajectory_1.probability * trajectory_2.probability
```


Side Notes:

Type Hinting

You might notice that we're using type hinting in Python. It gives somewhat of a "stronger type" feeling to python so that we can define what type of argument we pass to functions. It should give more clarity about what's happening, but it still acts like real Python so don't worry too much. 

https://docs.python.org/3/library/typing.html

Testing Efficiency

We will be testing the efficiency of your code by checking that it is O(n log n) through timing. We will be using the timeout-decorator for timing. If you're curious as to what to run, please check the github page:

https://github.com/pnpnpn/timeout-decorator

Assumptions

* All starting and end points are distinct!

* All starting and end points are represented by a tuple: (s, alpha) where s is in {0, 1, 2} which specifies the side of the triangle (in clockwise order) and 0 <= alpha <= 1 specifies how far along the side the point is (also in clockwise order).


