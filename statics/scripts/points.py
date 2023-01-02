# from platform import node
import numpy as np
# import pandas as pd
# from abc import ABC, abstractmethod
# import random
# import pysnooper


class Point:

    def __init__(self, id, coordinates, material):

        self.id = id
        self.coordinates = np.array(coordinates)
        self.x, self.y, self.z = self.coordinates
        # self.material = material

    def __str__(self):
        return f"point {self.id} at {self.coordinates}"

    def __repr__(self):
        return f"point {self.id} at {self.coordinates}"
