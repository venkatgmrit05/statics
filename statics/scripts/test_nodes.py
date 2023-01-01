from points import Point
from materials import Material
from beams import Beam
from nodes import Node
import unittest
# import pytest
import random
import sys
# import os

path_to_module = r".\statics\scripts"
sys.path.append(path_to_module)


class TestNodes(unittest.TestCase):

    variables_to_display = []
    # @pysnooper.snoop()

    def display_variables(_list):

        for item in _list:
            print(f"{item.__str__()} >> {item}")

    density = 1
    yield_strength = 1
    ultimate_strength = 1
    poisson_ratio = 1
    steel = Material(1, "steel", density, yield_strength,
                     ultimate_strength, poisson_ratio)

    coordinates1 = [1, 1, 1]
    point1 = Point(1, coordinates1, steel)
    node1 = Node(1, point1)

    coordinates2 = [2, 2, 2]
    point2 = Point(2, coordinates2, steel)
    node2 = Node(2, point2)

    beam_12 = Beam(1, 'beam_12', node1=node1, node2=node2)
    print(beam_12)

    beam_12.node1.forces = [10, -1, 1]
    beam_12.node2.forces = [-10, 1, 2]

    beam_12_in_eqm = beam_12.stable_static_equilibrium
    print(beam_12_in_eqm)

    # creating random coordinates
    rand_x = [random.randint(1, 20) for i in range(20)]
    rand_y = [random.randint(1, 20) for i in range(20)]
    rand_z = [random.randint(1, 20) for i in range(20)]

    rand_coords = list(zip(rand_x, rand_y, rand_z))

    # creating points
    points_dict = {}
    for i, rc in enumerate(rand_coords):
        points_dict[f"point{i}"] = rc

    # creating forces
    forces_dict = {}
    for i, rc in enumerate(rand_coords):
        forces_dict[f"force{i}"] = list(rc)

    # creating force variables
    f1 = forces_dict['force1']
    f2 = forces_dict['force2']
    f3 = forces_dict['force3']
    f4 = forces_dict['force4']
    f5 = forces_dict['force5']
    f6 = forces_dict['force6']
    # points = {}

    # Point objects
    p1 = Point(1, points_dict['point1'], steel)
    p2 = Point(2, points_dict['point2'], steel)
    p3 = Point(3, points_dict['point3'], steel)
    p4 = Point(4, points_dict['point4'], steel)
    p5 = Point(5, points_dict['point5'], steel)
    p6 = Point(6, points_dict['point6'], steel)
    # Node objects
    n1 = Node(1, p1, forces=f1)
    n2 = Node(2, p2, forces=f2)
    n3 = Node(3, p3, forces=f3)
    n4 = Node(4, p4, forces=f4)
    n5 = Node(5, p5, forces=f5)
    n6 = Node(6, p6, forces=f6)

    # Beam objects
    b1 = Beam(12, 'b1', node1=n1, node2=n2)
    b2 = Beam(23, 'b2', node1=n3, node2=n4)
    b3 = Beam(34, 'b3', node1=n5, node2=n6)

    variables_to_display.extend([n1, n2, n1.forces, n2.forces, n2.forces])

    # n2.connect(n3)
    # n3.connect(n5)

    variables_to_display.extend([n1, n2, n1.forces, n2.forces, n2.forces])
    variables_to_display.extend([n1.connected_nodes, n2.connected_nodes])
    # display_variables(variables_to_display)

    def test_dothis(self):

        print("!!!!!")

    def test_connect_3nodes(self, n2=n2, n3=n3, n5=n5):

        n2.connect(n3)
        n3.connect(n5)

        self.assertIn(n2.id, n3.connected_node_ids)
        self.assertIn(n2.id, n5.connected_node_ids)
        self.assertIn(n3.id, n2.connected_node_ids)
        self.assertIn(n3.id, n5.connected_node_ids)
        self.assertIn(n5.id, n3.connected_node_ids)
        self.assertIn(n5.id, n2.connected_node_ids)

    def test_connect_2nodes(self, n2=n2, n3=n3):

        n2.connect(n3)

        self.assertIn(n2, n3.connected_nodes)
        self.assertIn(n3, n2.connected_nodes)

        self.assertIn(n2.id, n3.connected_node_ids)
        self.assertIn(n3.id, n2.connected_node_ids)


if __name__ == '__main__':

    unittest.main()
    # unittest.TestNodes()
    # TestNodes()
