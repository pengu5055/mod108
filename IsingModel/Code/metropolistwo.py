"""
Rewrite of the Metroplis algorithm for a 2D Ising model.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterable

class Metropolis2:
    def __init__(self,
                 dimensions: tuple,
                 temperature: float,
                 # state_bounds: tuple,
                 quiet: bool = False,
                 ) -> None:
        self.x_dim, self.y_dim = dimensions
        self.temperature = temperature
        # self.state_bounds = (state_bounds[0], state_bounds[1] + 1)

        states = []
        for i in range(10000):
            self.state = np.random.choice([-1, 1], (self.x_dim, self.y_dim))
            states.append(self.state)


        self.states = np.array(states).mean(axis=0)

