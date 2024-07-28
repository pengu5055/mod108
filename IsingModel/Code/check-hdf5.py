"""
Check HDF5 file
"""
import numpy as np
import h5py

# Load the file
save_path = "./IsingModel/Results/avgE-vs-T-pool.h5"
with h5py.File(save_path, "r") as f:
    num_runs = len(f.keys())
    print(f"Number of runs: {num_runs}")
    print(f"Keys: {list(f.keys())}")


