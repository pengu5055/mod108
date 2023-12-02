"""
Gather the data required to plot the histogram of the final energies of the
chains.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import socket
from mpi4py import MPI
from simcityone import SimCity_1D

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Initialize the parameters
length = 17
temperature = 1
state_bounds = (-18, 0)
N = int(10e6)

# Distribute order of chains to run
M = 12
per_rank = M // size
remainder = M % size
QUEUE = np.array([per_rank] * size)

for i in range(remainder):
    QUEUE[i] += 1

if rank == 0:
    print(f"Queue: {QUEUE}")
    print(f"Total: {np.sum(QUEUE)}")

# Run the chains
energies = []
for i in range(QUEUE[rank]):
    sc = SimCity_1D(length, temperature, state_bounds, quiet=True)
    states, en = sc.run(N)
    energies.append(en[-1])

# Gather the data
data = comm.gather(energies, root=0)

# From here on, only the root process will run
if rank == 0:
    # Flatten the data
    data = np.array(data).flatten()
    
    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(data, columns=["Energy"])
    df.to_csv("./MolecularChain/Results/energies.csv", index=False)
    
    # Finalize MPI
    MPI.Finalize()
