# from platform import node
import numpy as np
# import pandas as pd
# from abc import ABC, abstractmethod
# import random
# import pysnooper
# import json

# json.load(r".")
tol = 6  # TODO should be controlled in config file


class Beam:
    # TODO documentation
    # TODO tests
    def __init__(self, id, name, **kwargs):

        self.id = id
        self.name = name
        if 'node1' in kwargs:  # TODO change node1,node2 to node_a,node_b
            self.node1 = kwargs['node1']
            self.node1.connected_beams.append(self)
            # self.node1.forces = [0,0,0]
        else:
            raise Exception("Beam object must have at least one node")
        if 'node2' in kwargs:
            self.node2 = kwargs['node2']
            self.node2.connected_beams.append(self)
            # self.node2.forces = [0,0,0]
        else:
            self.node2 = None
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            if self.node2:
                self.length = self.get_beam_length()
            else:
                raise Exception(
                    "Beam object must be initalized with either node2\
                         or length")

        self.nodes = [self.node1, self.node2]
        self.x_total = 0
        self.y_total = 0
        self.z_total = 0

        self.stable_static_equilibrium = None
        if self.node1 and self.node2:
            self.stable_static_equilibrium = self._is_in_stable_equllibrium()

        self._get_net_forces()

    def _get_net_forces_in_dir(self, _dir):

        dict_dir = {'x': 0, 'y': 1, 'z': 2}  # TODO should be global attr

        forces_in_dir = list(zip(
            self.node1.forces, self.node2.forces))[dict_dir[_dir]]

        sum_forces_in_dir = sum(forces_in_dir)

        return sum_forces_in_dir

    def _get_net_forces(self):
        self.net_forces = sum(
            [self._get_net_forces_in_dir(i) for i in ['x', 'y', 'z']])

    def get_beam_length(self):
        length = 0
        try:
            if self.node2 and self.node1:
                length = np.sqrt(
                    sum(map(lambda x: (x[0]-x[1])**2,
                        list(zip(self.node1.coordinates,
                            self.node2.coordinates)))))
            return np.round(length, tol)
        except ValueError as ve:
            print(f"error >> {ve}")

    def _is_in_x_equllibrium(self):
        net_forces_in_x = self._get_net_forces_in_dir('x')
        if net_forces_in_x:
            self.x_total = net_forces_in_x
            is_in_x_equllibrium = False
        else:
            self.x_total = net_forces_in_x
            is_in_x_equllibrium = True

        return is_in_x_equllibrium

    def _is_in_y_equllibrium(self):
        net_forces_in_y = self._get_net_forces_in_dir('y')
        if net_forces_in_y:
            self.y_total = net_forces_in_y
            is_in_y_equllibrium = False
        else:
            self.y_total = net_forces_in_y
            is_in_y_equllibrium = True

        return is_in_y_equllibrium

    def _is_in_z_equllibrium(self):

        net_forces_in_z = self._get_net_forces_in_dir('z')
        if net_forces_in_z:
            self.z_total = net_forces_in_z
            is_in_z_equllibrium = False
        else:
            self.z_total = net_forces_in_z
            is_in_z_equllibrium = True

        return is_in_z_equllibrium

    def _is_in_stable_equllibrium(self):

        self.is_in_stable_equllibrium = False
        if self._is_in_x_equllibrium()\
                and self._is_in_y_equllibrium()\
                and self._is_in_z_equllibrium():
            self.is_in_stable_equllibrium = True

        return self.is_in_stable_equllibrium

    def __repr__(self):
        return f"Beam <id {self.id}> <n1 {self.node1.id}> <n2 {self.node2.id}>"

    def __str__(self):
        return f"Beam between\
             nodes {self.node1.id} , {self.node2.id} with length {self.length}"


if __name__ == "__main__":
    # TODO create a test case
    # TODO add comprehensive tests
    # XXX write out full doc on how the beam forces and  moments are computed
    '''
    TODO
    i dont see any place wherr moments are being compouted. maybe they arent 
    needed because this is simply a beam so alinear sum of focres and moments 
    is sufficeint.
    asceratin this
    create a ticket and close when done for proof of work


    '''
