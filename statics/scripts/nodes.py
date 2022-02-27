# from platform import node
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
import random
import pysnooper


tol = 6

class Node:

    def __init__(self, id, point, forces =[0,0,0],moments =[0,0,0]):

        self.id = id
        self.material = point.material
        self.coordinates = point.coordinates
        self.connected = True
        self.connected_nodes = []
        self.connected_node_ids = []
        self.connected_beams = [] #TODO should popoulate when beam is instantiated
        self.forces = np.array(forces)
        self.moments = np.array(moments)

    #TODO consider splitting setting connections into two part process
    # connect_node/beam --> collect all connections to be applied together in batch
    # apply_connections
    
    def connect(self,entity):#TODO consider creatng entity abstract class

        if isinstance(entity,Node):
            # if entity not in self.connected_nodes:
            self.set_connection_node_node(entity)
        # if isinstance(entity,Beam): # TODO why? doesnt make sense
            self.set_connection_node_beam(entity) #TODO update newly connected beams
            self._transmit_connections()#TODO apply connecions to previously existing connections

    def set_connection_node_node(self, node_to_connect):

        self._collect_node_id(node_to_connect) 
        self._collect_node(node_to_connect)
        self._match_node_coordinates(node_to_connect)
        self._match_node_material(node_to_connect)
        self._match_node_forces(node_to_connect)
        self._match_node_moments(node_to_connect)

        #transmit changes to node2
        node_to_connect._collect_node_id(self)
        node_to_connect._collect_node(self)
    # @pysnooper.snoop()
    def _transmit_connections(self):

        # when a node connects to another node
        # it must update the state information for all the previously connected
        # nodes

        _connected_nodes = self.connected_nodes.copy()
        
        while _connected_nodes:
            # print(_connected_node)
            _n1 = _connected_nodes.pop()
            for _n2 in _connected_nodes:
                _n1.connect(_n2)

    def set_connection_node_beam(self,beam):
        pass

    def _match_node_coordinates(self, node_to_match):
        
        self.coordinates = node_to_match.coordinates

    def _collect_node(self,node_to_match):
        # TODO possible infinite loop ; consider placing
        # pre-existing check
        if node_to_match not in self.connected_nodes:
            self.connected_nodes.append(node_to_match)

    # @pysnooper.snoop()
    def _collect_node_id(self, node_to_match):

        # TODO possible infinite loop ; consider placing
        # pre-existing check
        if node_to_match.id not in self.connected_node_ids:
            self.connected_node_ids.append(node_to_match.id)

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
        return f"node {self.id}"
    
    def __repr__(self):
        return f"node {self.id}"

if __name__ == '__main__':
    print('ok')