"""
Check HDF5 file. Something looks way off...
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py

# Calculate Observables: Eigenmagnetization
def magnetization(state: np.ndarray):
    S = np.array([np.sum(np.array(final)) for final in state]) 
    return S

def susceptibility(states: np.ndarray, temperature: np.ndarray):
    chi = lambda energy: np.var(energy) / (temperature * energy.shape[0])
    output = np.array([chi(state[i]) for i in range(1) for state in states])
    return output

def heat_capacity(states: np.ndarray, temperature: np.ndarray):
    C = lambda energy: np.var(energy) / (temperature**2 * energy.shape[0])
    output = np.array([C(state[i]) for i in range(1) for state in states])
    return output


# Load the file
save_path = "./IsingModel/Results/H-expanded.h5"
H_values = np.loadtxt("./IsingModel/Code/H_range.lst")
energies = []
with h5py.File(save_path, "r") as f:
    # for block in np.arange(10, 100, 10):
        for H in H_values:
            key = f"{H}-0"
            group = f[key]
            energies.append(group[f"energy-{key}"][80002:])

energies = np.array(energies)
print(energies.shape)
np.save("./IsingModel/Results/E-expanded.npy", energies)

        
 