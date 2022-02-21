from platform import node
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
import random
import pysnooper

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
    
    def __str__(self):
        return f"point {self.id} at {self.coordinates}"
    
    def __repr__(self):
        return f"point {self.id} at {self.coordinates}"


class Node:

    def __init__(self, id, point, forces =[0,0,0],moments =[0,0,0]):

        self.id = id
        self.material = point.material
        self.coordinates = point.coordinates
        self.connected = True
        self.connected_nodes = []
        self.connected_beams = [] #TODO should popoulate when beam is instantiated
        self.forces = np.array(forces)
        self.moments = np.array(moments)

    #TODO consider splitting setting connections into two part process
    # connect_node/beam --> collect all connections to be applied together in batch
    # apply_connections
    
    def connect(self,entity):#TODO consider creatng entity abstract class

        if isinstance(entity,Node):
            self.set_connection_node_node(entity)
        # if isinstance(entity,Beam): # TODO why? doesnt make sense
            self.set_connection_node_beam(entity) #TODO update newly connected beams
            self._transmit_connections()#TODO apply connecions to previously existing connections

    def set_connection_node_node(self, node_to_connect):

        self._collect_node_id(node_to_connect)  
        self._match_node_coordinates(node_to_connect)
        self._match_node_material(node_to_connect)
        self._match_node_forces(node_to_connect)
        self._match_node_moments(node_to_connect)

        #transmit changes to node2
        node_to_connect._collect_node_id(self)

    def _transmit_connections(self):
        pass    

    def set_connection_node_beam(self,beam):
        pass

    def _match_node_coordinates(self, node_to_match):
        
        self.coordinates = node_to_match.coordinates

    # @pysnooper.snoop()
    def _collect_node_id(self, node_to_match):

        self.connected_nodes.append(node_to_match.id)

    def _match_node_material(self,node_to_match):
        
        self.material =node_to_match.material
    
    def _match_node_forces(self,node_to_match):
        
        _resultant_forces = self.forces + node_to_match.forces # in global coords
        self.forces = _resultant_forces
        node_to_match.forces = _resultant_forces

    def _match_node_moments(self,node_to_match):

        _resultant_moments = self.moments + node_to_match.moments # in global coords
        self.moments = _resultant_moments
        node_to_match.moments = _resultant_moments

    def __str__(self):
        return f"node {self.id} at {self.coordinates}"
    
    def __repr__(self):
        return f"node {self.id} at {self.coordinates}"


class Beam:
    # TODO documentation
    # TODO tests
    def __init__(self,id,name,**kwargs):

        self.id = id
        self.name = name 
        if 'node1' in kwargs:#TODO change node1,node2 to node_a,node_b
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
                raise Exception("Beam object must be initalized with either node2 or length")

        self.nodes = [self.node1, self.node2]
        self.x_total = 0
        self.y_total = 0
        self.z_total = 0

        self.stable_static_equilibrium = None
        if self.node1 and self.node2:
            self.stable_static_equilibrium = self._is_in_stable_equllibrium()

        self._get_net_forces()

    def _get_net_forces_in_dir(self,_dir):
        
        dict_dir = {'x':0,'y':1,'z':2}

        forces_in_dir = list(zip(
            self.node1.forces,self.node2.forces))[dict_dir[_dir]]
        
        sum_forces_in_dir = sum(forces_in_dir)

        return sum_forces_in_dir

    def _get_net_forces(self):
        self.net_forces = sum(
            [ self._get_net_forces_in_dir(i) for i in ['x','y','z']])

    def get_beam_length(self):
        length=0
        try:
            if self.node2 and self.node1:
                length = np.sqrt(
                    sum(map(lambda x: (x[0]-x[1])**2,
                        list(zip(self.node1.coordinates,self.node2.coordinates)))))
            return np.round(length,tol)
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
        net_forces_in_y =  self._get_net_forces_in_dir('y')
        if net_forces_in_y:
            self.y_total = net_forces_in_y
            is_in_y_equllibrium = False
        else:
            self.y_total = net_forces_in_y
            is_in_y_equllibrium = True
        
        return is_in_y_equllibrium

    def _is_in_z_equllibrium(self):
        
        net_forces_in_z =  self._get_net_forces_in_dir('z')
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
             and self._is_in_y_equllibrium() and self._is_in_z_equllibrium():
            self.is_in_stable_equllibrium = True


        return self.is_in_stable_equllibrium

    def __repr__(self):
        return f"Beam <id {self.id}> <n1 {self.node1.id}> <n2 {self.node2.id}>"

    def __str__(self):
        return f"Beam between\
             nodes {self.node1.id} , {self.node2.id} with length {self.length}"

class EntityConnect(ABC):

    @abstractmethod
    def connect_entities(self,mode):
        pass
    
    @abstractmethod
    def update_connections(self):
        pass
    
    @abstractmethod
    def update_entity_forces(self):
        pass

    @abstractmethod
    def update_entity_moments(self):
        pass

# class NodeConnector(EntityConnect):

#     def __init__(self,nodes):
#         self.nodes = nodes
    
#     def connect_entities(self):
        
#         for node in self.nodes:
#             self.connect_nodes(node)








if __name__ == '__main__':

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
    # n1.set_connection_node_node(n2)

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





