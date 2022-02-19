class Matter:
    pass

class Material:
    pass


class Node:

    def __init__(self,material,connected_nodes,connected_beams):
        self.material = material
        self.connected = True
        self.connected_nodes = connected_nodes
        self.connected_beams = connected_beams
        self.coordinates = None
        self.external_forces = []
        self.stable_static_equilibrium = self.is_in_stable_equllibrium()

    def set_connections(self):
        for node in self.connected_nodes:
            self.set_connection_node_node(node)

        for beam in self.connected_beams:
            self.set_connection_node_beam(beam)

    def set_connection_node_beam(self, node):
        pass

    def set_connection_node_beam(self,beam):
        pass

    def is_in_stable_equllibrium(self):
        
        self.is_in_stable_equllibrium = False
        if self.is_in_x_equllibrium() and self.is_in_y_equllibrium() and self.is_in_z_equllibrium() :
            self.is_in_stable_equllibrium = True
        
        return self.is_in_x_equllibrium
            
