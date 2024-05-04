"""
A rewrite of the metropolis algorithm written at a later date.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterable

class Metropolis1:
    def __init__(self,
                 length: int,
                 temperature: float,
                 state_bounds: tuple,
                 states: Iterable = None,
                 quiet: bool = False,
                 wait_for_execution: bool = False,
                 ) -> None:
        self.ALPHA = 1
        self.DELTA = 1
        self.EPS = 1e-6

        self.length = length
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
        self.init_state = np.copy(self.state)

        if not wait_for_execution:
            self.run()

    def _randomize_state(self) -> None:
        self.state = np.random.randint(self.state_bounds[0], self.state_bounds[1], self.length)
        self.state[0] = self.state[-1] = 0  # Fixed boundary conditions

    def _energy(self) -> float:
        energy = 0
        for i in range(self.length - 1):
            term1 = self.ALPHA * self.state[i]
            term2 = 0.5 * (self.state[i+1] - self.state[i])**2
            energy += term1 + term2
    
        return energy
    
    def _delta_energy(self, loc, delta_sign, prev_energy) -> float:
        """
        Calculate the change in energy for a given move.
        """
        # Calculate the change in energy
        delta = self.DELTA * delta_sign
        
        # Assert periodic boundary conditions
        if (loc - 1) >= 0:
            element1 = self.state[loc - 1]
        else:
            element1 = self.state[-1]
        if (loc + 1) <= self.length:
            element2 = self.state[loc + 1]
        else:
            element2 = self.state[0]

        new_energy = delta**2 - self.ALPHA * delta * (element1 - 2*self.state[loc] + element2)
        delta_energy = new_energy - prev_energy

        return delta_energy
    
    def run(self, N: int) -> tuple:
        """
        Run the Metropolis algorithm until average change over 5 steps is less than EPS.
        """
        self.energies = []
        self.energies.append(self._energy())
        step = 0

        # Main loop
        while True:
            if step % 100 == 0 and not self.quiet:
                print(f"Step: {step} / {N}")
            

            # Choose a random location in the chain
            # Avoid the fixed boundary conditions
            loc = np.random.randint(1, self.length - 1)

            # Impose state bounds
            if self.state[loc] == self.state_bounds[0]:
                delta_sign = 0
            elif self.state[loc] == self.state_bounds[1] - 1:
                delta_sign = 0

            # If valid move, change state at loc
            sign = 1 if np.random.rand() < 0.5 else -1
            self.state[loc] += sign * self.DELTA

            # Calculate energy change
            delta_energy = self._delta_energy(loc, sign, self.energies[step - 1])

            # Accept or reject move
            if delta_energy < 0:
                self.energies.append(self.energies[step - 1] + delta_energy)
            
            # If energy is higher, accept with probability exp(-delta_energy / kT)
            else:
                p = np.exp(-delta_energy / self.temperature)
                if np.random.rand() < p:
                    self.energies.append(self.energies[step - 1] + delta_energy)
                else:
                    # Roll back the change
                    self.state[loc] -= sign * self.DELTA
                    self.energies.append(self.energies[step - 1])


            # Exit condition - check for convergence
            if step > 5:
                if np.abs(np.mean(np.diff(self.energies[-5:]))) < self.EPS:
                    break

        if not self.quiet:
            print("Simulation complete.")
            print(f"Inital energy: {self.energies[0]}")
            print(f"Final energy: {self.energies[-1]}")
        
        return self.init_state, self.state, self.energies

