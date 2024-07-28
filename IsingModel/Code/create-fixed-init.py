"""
Create a NxN lattice with random spins and save it to a file
so it can be used as an initial state for the Ising model.
"""
import numpy as np

N = 500
state = np.random.choice([-1, 1], (N, N))
np.save("./IsingModel/Results/random-state.npy", state)
