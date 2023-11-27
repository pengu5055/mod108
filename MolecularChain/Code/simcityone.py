"""
Contains the base class for the 1D Metropolis algorithm 
implementation.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterable

class SimCity_1D:
    def __init__(self,
                 length: int,
                 temperature: float,
                 state_bounds: tuple,
                 states: Iterable = None
                 ) -> None:
        """
        Initialize the class. 

        It is assumed that each particle can take on a state described by a
        integer value. The state bounds are the minimum and maximum values
        that the state can take on. The state is initialized to a random
        configuration if no state is provided.
        """
        # Constants
        self.ALPHA = 1

        # Parameters
        self.length = length
        self.temperature = temperature
        self.state_bounds = (state_bounds[0], state_bounds[1] + 1)

        self.state = states
        if self.state is isinstance(self.state, Iterable):
            if len(self.state) != self.length:
                raise ValueError("The length of the state vector must be equal to the length of the chain.")
            else:
                pass
        else:
            self._randomize_state()
        
        self.state = np.array(self.state)

    def _randomize_state(self) -> None:
        """
        Randomize the state of the chain.
        """
        self.state = np.random.randint(self.state_bounds[0], self.state_bounds[1], self.length)

    def _energy(self) -> float:
        """
        Calculate the energy of the chain.
        """
        energy = 0
        for i in range(self.length - 1):
            term1 = self.ALPHA * self.state[i]
            term2 = 0.5 * (self.state[i+1] - self.state[i])**2
            energy += term1 + term2

        self.energy = energy

        return energy

        

