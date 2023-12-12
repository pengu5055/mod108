"""
Contains the base class for the 2D Metropolis algorithm 
implementation. Will also try to implement the Wolff algorithm.
Will also try to implement the Swendsen-Wang algorithm.
Will also try to MPI-ize the code.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Iterable
from mpi4py import MPI
import socket

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
        # Initialize MPI
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        # Constants
        self.J = 1  # Interaction energy
        self.H = 0  # External field

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

        print(f"[{self.rank}] Hello! I am process {self.rank} on {socket.gethostname()}. Ready to go to work!")

    def _randomize_state(self) -> None:
        """
        Randomize the state of the chain.
        """
        self.state = np.random.randint(self.state_bounds[0], self.state_bounds[1], (self.size, self.size))
        # self.state[0, :] = self.state[-1, :] = self.state[:, 0] = self.state[:, -1] = 0
    
    def _energy(self) -> float:
        """
        Calculate the energy of the chain.

        E = -J * sum_{i, j} s_i s_j - H * sum_{i} s_i
        """
        energy = 0
        # Sum over all pairs of points
        for i in range(self.size):
            for j in range(self.size):
                # Sum over all neighbors
                for k in range(i, self.size):
                    for l in range(j, self.size):
                        if (k, l) != (i, j):
                            term1 = -self.J * self.state[i, j] * self.state[k, l]
                            term2 = -self.H * self.state[i, j]
                            energy += term1 + term2
        
        self.energy = energy

        return energy

    def _delta_energy(self, loc) -> float:
        """
        Calculate the change in energy of the chain.

        The change in energy is calculated by considering the change in
        energy due to the change in state of the particle at the location
        specified by loc.
        """

        s0 = self.state[loc[0], loc[1]]
        s1 = self.state[loc[0] - 1, loc[1]]
        s3 = self.state[loc[0], loc[1] - 1]
        
        try:
            s2 = self.state[loc[0] + 1, loc[1]]
        except IndexError:
            # Do cyclic boundary conditions
            s2 = self.state[loc[0] + 1 - self.size, loc[1]]
        
        try:
            s4 = self.state[loc[0], loc[1] + 1]
        except IndexError:
            # Do cyclic boundary conditions
            s4 = self.state[loc[0], loc[1] + 1 - self.size]

        term1 = 2*self.J * s0 * (s1 + s2 + s3 + s4)
        term2 = 2*self.H * s0


        delta_energy = term1 + term2

        self.last_delta_energy = delta_energy

        return delta_energy
    
    def run(self, steps: int) -> tuple:
        """
        Run the simulation for the specified number of steps.
        """
        # NOTE: This calculation takes long for large grids, MPI it so 
        # that each process only calculates the energy of a portion of the
        # grid.
        self._energy()
        self.energies = [np.copy(self.energy)]
        self.last_delta_energy = 0

        for i in range(steps):
            previous = 0
            if i % 100 == 0 and not self.quiet:
                print(f"Step {i} of {steps}...")
            # Choose a random location in the chain.
            loc = np.random.randint(0, (self.size, self.size))
            previous = self.state[*loc]

            # Modify the state at that location.
            not_taken_states = np.delete(np.arange(self.state_bounds[0], self.state_bounds[1]), self.state[*loc])
            self.state[*loc] = np.random.choice(not_taken_states)

            # DEBUG PRINT:
            # if previous == 1: print(not_taken_states)
            
            # Calculate the change in energy.
            delta_energy = self._delta_energy(loc)

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
                    self.state[loc] = previous

            if changed:
                self.energy = changed

            self.energies.append(np.copy(self.energy))

        if not self.quiet:
            print(f"Initial energy: {self.energies[0]}")
            print(f"Final energy: {self.energy}")

        return self.state, self.energies
    
def construct_chunks(data: np.ndarray, size: int) -> tuple:
    """
    Construct a chunk of the grid to be calculated by the process.
    """
    # NOTE: This assumes that the grid is square.
    # NOTE: This assumes that the grid is divisible by the number of processes.

    # Calculate the number of rows per process.
    elements_per_chunk = data.shape[0] // size

    # Get start stop indices for chunks
    chunks = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            x_start = i * elements_per_chunk
            x_end = (i + 1) * elements_per_chunk
            y_start = j * elements_per_chunk
            y_end = (j + 1) * elements_per_chunk
            chunks.append((x_start, x_end, y_start, y_end))

    return chunks

def chunk_distributor(grid_size: int, num_nodes: int):
    """
    Distribute chunks of the grid to each process.
    """
    total_chunks = grid_size**2
    chunks_per_node = total_chunks // grid_size
    extra_chunks = total_chunks % num_nodes

