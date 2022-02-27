# from statics.statics.scripts.beams 
import numpy as np
import pandas as pd
import random
import sys
import os

cfp = r'D:\Data\OfficeWorkspace-20191016T044923Z-001\OfficeWorkspace\statics'
sys.path.append(cfp)


from statics.scripts.nodes import Node
from statics.scripts.beams import Beam
from statics.scripts.materials import Material
from statics.scripts.points import Point


if __name__ == "__main__":

    # rfp = os.path.realpath(__file__)
    # dirname = os.path.dirname(rfp)
    # sys.path.append("..\statics")


    variables_to_display =[]
    # @pysnooper.snoop()
    def display_variables(_list):

        for item in _list:
            print(f"{item.__str__()} >> {item}")


    density=1
    yield_strength=1
    ultimate_strength=1
    poisson_ratio =1
    steel = Material(1,"steel",density,yield_strength,ultimate_strength,poisson_ratio)

    coordinates1 = [1,1,1]
    point1 = Point(1,coordinates1,steel)
    node1 = Node(1,point1)

    coordinates2 = [2,2,2]
    point2 = Point(2,coordinates2,steel)
    node2 = Node(2,point2)

    beam_12 = Beam(1,'beam_12',node1=node1,node2=node2)
    print(beam_12)

    beam_12.node1.forces = [10,-1,1]
    beam_12.node2.forces = [-10,1,2]

    beam_12_in_eqm = beam_12.stable_static_equilibrium
    print(beam_12_in_eqm)

    # creating random coordinates
    rand_x = [ random.randint(1,20) for i in range(20)]
    rand_y = [ random.randint(1,20) for i in range(20)]
    rand_z = [ random.randint(1,20) for i in range(20)]

    rand_coords = list(zip(rand_x, rand_y, rand_z))

    #creating points
    points_dict = {}
    for i,rc in enumerate(rand_coords):
        points_dict[f"point{i}"]=rc

    #creating forces
    forces_dict = {}
    for i,rc in enumerate(rand_coords):
        forces_dict[f"force{i}"]=list(rc)

    #creating force variables
    f1 = forces_dict['force1']
    f2 = forces_dict['force2']
    f3 = forces_dict['force3']
    f4 = forces_dict['force4']
    f5 = forces_dict['force5']
    f6 = forces_dict['force6']
    # points = {}

    # Point objects
    p1 = Point(1,points_dict['point1'],steel)
    p2 = Point(2,points_dict['point2'],steel)
    p3 = Point(3,points_dict['point3'],steel)
    p4 = Point(4,points_dict['point4'],steel)
    p5 = Point(5,points_dict['point5'],steel)
    p6 = Point(6,points_dict['point6'],steel)
    # Node objects
    n1 = Node(1,p1,forces=f1)
    n2 = Node(2,p2,forces=f2)
    n3 = Node(3,p3,forces=f3)
    n4 = Node(4,p4,forces=f4)
    n5 = Node(5,p5,forces=f5)
    n6 = Node(6,p6,forces=f6)

    # Beam objects
    b1 = Beam(12,'b1',node1=n1,node2=n2)
    b2 = Beam(23,'b2',node1=n3,node2=n4)
    b3 = Beam(34,'b3',node1=n5,node2=n6)

    variables_to_display.extend([n1,n2,n1.forces,n2.forces,n2.forces])

    n2.connect(n3)
    n3.connect(n5)

    variables_to_display.extend([n1,n2,n1.forces,n2.forces,n2.forces])
    variables_to_display.extend([n1.connected_nodes,n2.connected_nodes])
    # display_variables(variables_to_display)



    # count = 0
    # nodes_dict = {}
    # for _p,_c in points_dict.items():
    #     nodes_dict[f"node{count}"] = #











    #create variables from the dict
    # for k,v in points_dict.items():
    #     var_name = eval(k)
    #     exec(f'var_name = {v}')
    #     print(var_name)

    # def set_variables_from_dict(_dict):
    #     for k,v in _dict.items():
    #         exec

    # set_variables_from_dict(points_dict)





