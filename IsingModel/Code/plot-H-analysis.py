"""
Plot the average relaxation energy of the system as a function of temperature.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import h5py
import cmasher as cmr
import palettable as pl

# Enable custom stylesheet
plt.style.use('./ma-style.mplstyle')
mpl.use("qtagg")

# Simulation parameters
save_path = "./IsingModel/Results/H-analysis.h5"
bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)
T_values = np.loadtxt("./IsingModel/Code/H_range.lst")

# Containers for data
end_energy = []
end_states = []


# Load data
with h5py.File(save_path, "r") as f:
    num_runs = 100

    for i, T in enumerate(T_values):
        row_states = []
        row_end_energy = []

        for run in range(num_runs):
            key = f"{T}-{run}"
            group = f[key]
            row_states.append(group[f"state-{key}"][:])
            row_end_energy.append(group[f"energy-{key}"][-1])

        end_states.append(row_states) 
        end_energy.append(row_end_energy)

# Calculate statistics
end_energy = np.array(end_energy)
avg_energy = np.mean(end_energy, axis=1)
sigma_energy = np.std(end_energy, axis=1)

def magnetization(state: np.ndarray):
    S = np.array([[np.sum(np.array(final[run])) for run in range(num_runs)] for final in end_states]) 
    return S

S = np.abs(magnetization(end_states))
avgS = np.mean(S, axis=1)
sigmaS = np.std(S, axis=1)

# Calculate observables: Spin susceptibility and Heat capacity from truncated data
def susceptibility(energy: np.ndarray, temperature: np.ndarray):
    
    chi = lambda energy: np.var(energy) / (temperature * energy.shape[0]*energy.shape[1])
    output = np.array([chi(state[i]) for i in range(num_runs) for state in end_states])
    return output

def heat_capacity(energy: np.ndarray, temperature: np.ndarray):
    C = lambda energy: np.var(energy) / (temperature**2 * energy.shape[0]*energy.shape[1])
    output = np.array([C(state[i]) for i in range(num_runs) for state in end_states])
    return output
