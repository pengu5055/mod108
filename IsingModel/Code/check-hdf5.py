"""
Check HDF5 file. Something looks way off...
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py

# Calculate Observables: Eigenmagnetization
def magnetization(state: np.ndarray):
    S = np.array([[np.sum(np.array(final[run])) for run in range(1)] for final in state]) 
    return S


# Load the file
save_path = "./IsingModel/Results/H-analysis-v2.h5"
H_values = np.loadtxt("./IsingModel/Code/H_range.lst")
energies = []
S = []
with h5py.File(save_path, "r") as f:
    # for block in np.arange(10, 100, 10):
        for H in H_values:
            key = f"{H}-0"
            group = f[key]
            S.append(magnetization(group[f"state-{key}"][:]))
            energies.append(group[f"energy-{key}"][80002:])
    
S = np.array(S)
energies = np.array(energies)
np.save("./IsingModel/Results/S-v2.npy", S)
np.save("./IsingModel/Results/E-v2.npy", energies)
        
 