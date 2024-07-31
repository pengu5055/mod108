"""
Check HDF5 file. Something looks way off...
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py


# Load the file
save_path = "./IsingModel/Results/H-analysis-noanneal.h5"
with h5py.File(save_path, "r") as f:
    key = list(f.keys())
    print(len(key))

