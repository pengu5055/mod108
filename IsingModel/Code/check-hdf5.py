"""
Check HDF5 file. Something looks way off...
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py


# Load the file
save_path = "./IsingModel/Results/H-analysis-v2.h5"
T_values = np.loadtxt("./IsingModel/Code/T_range.lst")

with h5py.File(save_path, "r") as f:
    for T in T_values:
        key = f"{T}-0"
        group = f[key]
        
 