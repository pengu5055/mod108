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
        self.DELTA = 1  # Change in state

        # Parameters
        self.length = length
        self.temperature = temperature
        self.state_bounds = (state_bounds[0], state_bounds[1] + 1)

        self.state = states

        if isinstance(self.state, list | tuple | np.ndarray):
            if len(self.state) == self.length:
                self.state = states
            else:
                raise ValueError("The length of the state vector must be equal to the length of the chain.")
        else:
            print("No state provided. Randomizing state...")
            self._randomize_state()
        
        self.state = np.array(self.state)

    def _randomize_state(self) -> None:
        """
        Randomize the state of the chain.
        """
        self.state = np.random.randint(self.state_bounds[0], self.state_bounds[1], self.length)
        self.state[0] = self.state[-1] = 0

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

    def _delta_energy(self, loc, delta_sign) -> float:
        """
        Calculate the change in energy of the chain.

        The change in energy is calculated by considering the change in
        energy due to the change in state of the particle at the location
        specified by loc.
        """
        pre = post = 0
        term1 = self.DELTA**2
        term2 = self.ALPHA * delta_sign * self.DELTA * (pre - 2*self.state[loc] + post)

        try:
            pre = self.state[loc + 1]
        except IndexError:
            if not self.quiet:
                print(f"The location {loc} is at the end of the chain.")
                # Loop around to the beginning of the chain.
                pre = self.state[0]
        try:
            post = self.state[loc - 1]
        except IndexError:
            if not self.quiet:
                print(f"The location {loc} is at the beginning of the chain.")
                # Loop around to the end of the chain.
                post = self.state[-1]

        # Watch out for minus sign!
        delta_energy = term1 + term2

        self.last_delta_energy = delta_energy

        return delta_energy

    def run(self, steps: int, quiet: bool = False) -> tuple:
        """
        Run the simulation for the specified number of steps.
        """
        self.quiet = quiet
        self._energy()
        self.energies = [np.copy(self.energy)]
        self.last_delta_energy = 0

        for i in range(steps):
            if i % 100 == 0 and not self.quiet:
                print(f"Step {i} of {steps}...")
            # Choose a random location in the chain.
            # Currently not allowing the first or last particle to move.
            loc = np.random.randint(1, self.length - 1)

            if self.state[loc] == self.state_bounds[0]:
                # If the state is already at the lower bound, don't allow it
                # to go lower.
                continue
            # State bounds 1 are inclusive, so we need to subtract 1.
            elif self.state[loc] == self.state_bounds[1] - 1:
                # If the state is already at the upper bound, don't allow it
                # to go higher.
                continue

            # Modify the state at that location.
            sign = 1 if np.random.rand() < 0.5 else -1
            self.state[loc] += sign * self.DELTA

            # Calculate the change in energy.
            delta_energy = self._delta_energy(loc, sign)

            # If the change in energy is negative, accept the change.
            changed = 0
            if delta_energy < 0:
                changed = self.energy + delta_energy

            # If the change in energy is positive, accept the change with
            # probability exp(-delta_energy / kT).
            else:
                p = np.exp(-delta_energy / self.temperature)
                # Roll probability.
                if np.random.rand() < p:
                    changed = self.energy + delta_energy
                else:
                    # Roll back the change.
                    self.state[loc] -= sign * self.DELTA

            if changed:
                self.energy = changed

            self.energies.append(self.energy)

        if not self.quiet:
            print(f"Initial energy: {self.energies[0]}")
            print(f"Final energy: {self.energy}")

        return self.state, self.energies
    