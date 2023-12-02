"""
Contains the base class for the 2D Metropolis algorithm 
implementation. Will also try to implement the Wolff algorithm.
Will also try to implement the Swendsen-Wang algorithm.
Will also try to MPI-ize the code.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterable


class SimCity_2D:
    def __init__(self,
                 size: int,
                 temperature: float,
                 state_bounds: tuple,
                 states: Iterable = None,
                 quiet: bool = False
                 ) -> None:
        """
        Initialize the class. 

        It is assumed that each grid point can take on a state described by a
        integer value. The state bounds are the minimum and maximum values
        that the state can take on. The state is initialized to a random
        configuration if no state is provided.
        """
        # Parameters
        self.size = size
        self.temperature = temperature
        self.state_bounds = (state_bounds[0], state_bounds[1] + 1)

        self.state = states
        self.quiet = quiet

        if isinstance(self.state, list | tuple | np.ndarray):
            if len(self.state) == self.length:
                self.state = states
            else:
                raise ValueError("The length of the state vector must be equal to the length of the chain.")
        else:
            if not self.quiet:
                print("No state provided. Randomizing state...")
            self._randomize_state()
        
        self.state = np.array(self.state)

    def _randomize_state(self) -> None:
        """
        Randomize the state of the chain.
        """
        self.state = np.random.randint(self.state_bounds[0], self.state_bounds[1], (self.size, self.size))
        # self.state[0, :] = self.state[-1, :] = self.state[:, 0] = self.state[:, -1] = 0