class NodeConnector(EntityConnect):

    def __init__(self,nodes):
        self.nodes = nodes
    
    def connect_entities(self):
        
        for node in self.nodes:
            self.connect_nodes(node)

