import numpy as np
import pandas as pd

tol = 6
class Matter:
    def __init__(self):
        pass

class Material:
    
    def __init__(self,id,name,density,yield_strength,ultimate_strength,poisson_ratio):
        
        self.id = id
        self.name = name
        self.density = density
        self.yield_strength = yield_strength
        self.ultimate_strength = ultimate_strength
        self.poisson_ratio = poisson_ratio

class Point:

    def __init__(self,id,coordinates,material):

        self.id = id
        self.coordinates = np.array(coordinates)
        self.x,self.y,self.z = self.coordinates
        self.material = material

class Node:

    def __init__(self,
        id,point,connected_nodes=[],connected_beams=[],forces =[],moments =[]):

        self.id = id
        self.material = point.material
        self.coordinates = point.coordinates
        self.connected = True
        self.connected_nodes = connected_nodes
        self.connected_beams = connected_beams
        self.forces = forces
        self.moments = moments


    def set_connections(self):
        for node in self.connected_nodes:
            self.set_connection_node_node(node)

        for beam in self.connected_beams:
            self.set_connection_node_beam(beam)

    def set_connection_node_beam(self, node):
        pass

    def set_connection_node_beam(self,beam):
        pass


class Beam:

    def __init__(self,id,name,**kwargs):

        self.id = id
        self.name = name 
        if 'node1' in kwargs:
            self.node1 = kwargs['node1']
        if 'node2' in kwargs:
            self.node2 = kwargs['node2']
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = self.get_beam_length()


        # self.stable_static_equilibrium = self.is_in_stable_equllibrium()

    def get_beam_length(self):

        try:
            if self.node2 and self.node1:
                length = np.sqrt(
                    sum(map(lambda x: (x[0]-x[1])**2,
                        list(zip(self.node1.coordinates,self.node2.coordinates)))))
        except ValueError as ve:
            print(f"error >> {ve}")
        
        return np.round(length,tol)

    def __repr__(self):
        return f"Beam between nodes {self.node1.id} , {self.node2.id} with length {self.length}"

    def __str__(self):
        return f"Beam between nodes {self.node1.id} , {self.node2.id} with length {self.length}"


    def is_in_x_equllibrium():
        pass
    def is_in_y_equllibrium():
        pass
    def is_in_z_equllibrium():
        pass

    def is_in_stable_equllibrium(self):
        
        self.is_in_stable_equllibrium = False
        if self.is_in_x_equllibrium()\
             and self.is_in_y_equllibrium() and self.is_in_z_equllibrium() :
            self.is_in_stable_equllibrium = True
        
        return self.is_in_stable_equllibrium


            
if __name__ == '__main__':

    density=1
    yield_strength=1
    ultimate_strength=1
    poisson_ratio =1
    # properties = [density, yield_strength,ultimate_strength,poisson_ratio]
    steel = Material(1,"steel",density,yield_strength,ultimate_strength,poisson_ratio)
    
    coordinates1 = [1,1,1]
    point1 = Point(1,coordinates1,steel)
    node1 = Node(1,point1)

    coordinates2 = [2,2,2]
    point2 = Point(2,coordinates2,steel)
    node2 = Node(2,point2)

    beam_12 = Beam(1,'beam_12',node1=node1,node2=node2)
    print(beam_12)





