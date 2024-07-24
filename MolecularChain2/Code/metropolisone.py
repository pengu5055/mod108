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
        self.MAX_ITER = 100000
        self.STOP_STEPS = 50
        self.EPS = 1e-10
        self.EXIT_COND2 = False
        self.EXIT_COND2_TOL = 0.85
        self.ANNEAL = True
        self.ANNEAL_RATE = 0.9999

        self.length = length
        self.temperature = temperature
        self.temperatures = [temperature]
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

        # if not wait_for_execution:
        #    self.run()

    def _randomize_state(self) -> None:
        self.state = np.random.randint(self.state_bounds[0], self.state_bounds[1], self.length)
        self.state[0] = self.state[-1] = 0  # Fixed boundary conditions

    def _energy(self) -> float:
        energy = 0
        for i in range(1, self.length - 1):
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

        # delta_energy = delta**2 - self.ALPHA * delta * (element1 - 2*self.state[loc] + element2)
        new_energy = -self.ALPHA * delta + 0.5*(element2 - self.state[loc] - delta)**2 + 0.5*(self.state[loc] + delta - element1)**2
        delta_energy = new_energy - prev_energy

        return delta_energy
    
    def run(self) -> tuple:
        """
        Run the Metropolis algorithm until sum of changes over self.STOP_STEPS steps is less than EPS.
        """
        self.energies = []
        self.energies.append(self._energy())
        step = 0

        # Main loop
        while True:            
            # Choose a random location in the chain
            # Avoid the fixed boundary conditions
            loc = np.random.randint(1, self.length - 1)

            # Get the sign of the change
            sign = 1 if np.random.rand() < 0.5 else -1

            # Impose state bounds (change sign if at boundary)
            if self.state[loc] == self.state_bounds[0]:
                sign = 0
            elif self.state[loc] == self.state_bounds[1] - 1:
                sign = 0

            # If valid move, change state at loc
            self.state[loc] += sign * self.DELTA

            # Calculate energy change
            # delta_energy = self._delta_energy(loc, sign, self.energies[step])
            # Temporary fix: Use whole for loop
            delta_energy = self._energy() - self.energies[step]

            # Accept or reject move
            if delta_energy < 0:
                self.energies.append(self.energies[step] + delta_energy)

                if self.ANNEAL:
                    self.temperature *= self.ANNEAL_RATE
            
            # If energy is higher, accept with probability exp(-delta_energy / kT)
            else:
                p = np.exp(-delta_energy / self.temperature)
                if np.random.rand() < p:
                    self.energies.append(self.energies[step] + delta_energy)
                else:
                    # Roll back the change
                    self.state[loc] -= sign * self.DELTA
                    self.energies.append(self.energies[step])


            # Exit condition - check for convergence
            if step > self.STOP_STEPS:
                exit_cond = np.sum(np.abs(np.diff(self.energies[-self.STOP_STEPS:])))
                exit_cond2 = self.energies[-1] <= np.min(self.energies) * self.EXIT_COND2_TOL if self.EXIT_COND2 else True
                if not self.quiet:
                    print(f"Step: {step}, Exit condition: {exit_cond}, Delta Energy: {delta_energy}", end="\r")
                if exit_cond < self.EPS and exit_cond2:
                    break
                elif step > self.MAX_ITER:
                    break

            # Increment step
            step += 1

            # Store temperature
            self.temperatures.append(self.temperature)

        # Remember number of steps needed
        self.sim_steps = step

        if not self.quiet:
            print("\n")
            print("Simulation complete.")
            print(f"Inital energy: {self.energies[0]}")
            print(f"Final energy: {self.energies[-1]}")
        
        return self.init_state, self.state, self.energies
