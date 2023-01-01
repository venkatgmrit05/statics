# from platform import node
# import numpy as np
# import pandas as pd
# from abc import ABC, abstractmethod
# import random
# import pysnooper

tol = 6


class Material:

    def __init__(self,
                 id, name, density, yield_strength,
                 ultimate_strength, poisson_ratio):

        self.id = id
        self.name = name
        self.density = density
        self.yield_strength = yield_strength
        self.ultimate_strength = ultimate_strength
        self.poisson_ratio = poisson_ratio
