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
        self.J = 1
        self.H = 0
        self.MAX_ITER = 1000000
        self.STOP_STEPS = 500
        self.STOP_ENERGIES = 100
        self.EPS = 1e-8
        self.quiet = quiet

        self.x_dim, self.y_dim = dimensions
        self.temperature = temperature
        # self.state_bounds = (state_bounds[0], state_bounds[1] + 1)

        self.state = np.random.choice([-1, 1], (self.x_dim, self.y_dim))
        self.init_state = np.copy(self.state)

    def _randomize_state(self) -> None:
        self.state = np.random.choice([-1, 1], (self.x_dim, self.y_dim))

    def _energy(self) -> float:
        energy = 0
        for i in range(self.x_dim):
            for j in range(self.y_dim):
                energy += -self.J * self.state[i, j] * (self.state[(i+1) % self.x_dim, j] + self.state[i, (j+1) % self.y_dim])

        if self.H:
            energy += -self.H * np.sum(self.state)
            
        return energy
    
    def _delta_energy(self, i, j, prev_energy) -> float:
        return 2 * self.J * self.state[i, j] * (self.state[(i-1) % self.x_dim, j] + 
                                                self.state[(i+1) % self.x_dim, j] + 
                                                self.state[i, (j-1) % self.y_dim] +
                                                self.state[i, (j+1) % self.y_dim]) + 2 * self.H * self.state[i, j]
    

    def run(self):
        self.energies = []
        self.energies.append(self._energy())

        iter = 0

        # Main loop
        while True:
            # Choose a random location in the chain
            i, j = np.random.randint(0, self.x_dim), np.random.randint(0, self.y_dim)
            delta_energy = self._delta_energy(i, j, self.energies[-1])
            
            if delta_energy <= 0:
                self.state[i, j] *= -1
            else:
                if np.random.rand() < np.exp(-delta_energy / self.temperature):
                    self.state[i, j] *= -1

            self.energies.append(delta_energy)
            if iter > self.STOP_STEPS:
                exit_cond = np.sum(np.abs(np.diff(self.energies[-self.STOP_ENERGIES:])))
                if exit_cond < self.EPS:
                       break
                if not self.quiet:
                    print(f"Step: {iter}, Exit condition: {exit_cond}, Delta Energy: {delta_energy}", end="\r")
            
            if iter > self.MAX_ITER:
                break

            iter += 1
        
        if not self.quiet:
            print("\n")
            print("Simulation complete.")
            print(f"Total steps: {iter}")
            print(f"Inital energy: {self.energies[0]}")
            print(f"Final energy: {self.energies[-1]}")

        return self.init_state, self.state, self.energies
                

