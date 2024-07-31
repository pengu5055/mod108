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
T_values = np.loadtxt("./IsingModel/Code/H_range.lst")

def susceptibility(states: np.ndarray, temperature: np.ndarray):
    chi = lambda energy: np.var(energy) / (temperature * energy.shape[0])
    # output = np.array([chi(state[i]) for i in range(1) for state in states])
    return chi(states)

def heat_capacity(states: np.ndarray, temperature: np.ndarray):
    C = lambda energy: np.var(energy) / (temperature**2 * energy.shape[0])
    # output = np.array([C(state[i]) for i in range(1) for state in states])
    return C(states)

energies = np.load("./IsingModel/Results/E-v2.npy")
energies_exp = np.load("./IsingModel/Results/E-expanded.npy")
H_values = np.loadtxt("./IsingModel/Code/H_range.lst")

# Calculate Observables
chi = [susceptibility(energy, 1) for energy in energies]
c = [heat_capacity(energy, 1) for energy in energies]
chi = np.array(chi)
c = np.array(c)

chi_exp = [susceptibility(energy, 1) for energy in energies_exp]
c_exp = [heat_capacity(energy, 1) for energy in energies_exp]
chi_exp = np.array(chi_exp)
c_exp = np.array(c_exp)

# Plot the data
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot Spin Susceptibility
ax[0].plot(H_values, chi, marker="o", color=colors[1], label=r"Spin Susceptibility $\chi$ $s=1/2$")
ax[0].plot(H_values, chi_exp, color=colors[3], label=r"Spin Susceptibility $\chi$ $s=3/2$", lw=1, ls="--")
ax[0].set_xlabel(r"Magnetic Field $H$")
ax[0].set_ylabel(r"Spin Susceptibility $\chi$")
ax[0].set_title(r"Spin Susceptibility vs. Magnetic Field")
ax[0].set_yscale("log")
ax[0].legend()

# Plot Heat Capacity
ax[1].plot(H_values, c, marker="o", color=colors[1], label=r"Heat Capacity $C$ $s=1/2$")
ax[1].plot(H_values, c_exp, color=colors[3], label=r"Heat Capacity $C$ $s=3/2$", lw=1, ls="--")
ax[1].set_xlabel(r"Magnetic Field $H$")
ax[1].set_ylabel(r"Heat Capacity $C$")
ax[1].set_title(r"Heat Capacity vs. Magnetic Field")
ax[1].set_yscale("log")
ax[1].legend()

plt.tight_layout()
plt.savefig("./IsingModel/Images/H-analysis.png")
plt.show()
