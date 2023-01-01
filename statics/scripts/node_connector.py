if __name__ == '__main__':

    # deprecated
    # TODO remove file after confirming deprectaion
    class NodeConnector():

        def __init__(self, nodes):
            self.nodes = nodes

        def connect_entities(self):

            for node in self.nodes:
                self.connect_nodes(node)
