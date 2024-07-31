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
save_path = "./IsingModel/Results/avgE-vs-T-expandedstate.h5"
bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)
T_values = np.loadtxt("./IsingModel/Code/T_range.lst")

# Containers for data
steps_to_convergence = []
end_energy = []
end_temperature = []
end_states = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = 100
    T1 = T_values[0]
    state1 = f[f"{T1}-0"][f"state-{T1}-0"][:]
    T2 = T_values[-1]
    state2 = f[f"{T2}-0"][f"state-{T2}-0"][:]


fig, ax = plt.subplots(1, 2, figsize=(12, 5))

norm = mpl.colors.Normalize(vmin=-2, vmax=2)
sm = plt.cm.ScalarMappable(cmap='PRGn', norm=norm)
im = ax[0].imshow(state1, cmap='PRGn', norm=norm)
cbar = plt.colorbar(sm, ax=ax[0])

ax[0].set_title(f"Initial state: T={T1}")
ax[0].set_xticks([])
ax[0].set_yticks([])
cbar.set_label("Spin value")

norm = mpl.colors.Normalize(vmin=-2, vmax=2)
sm = plt.cm.ScalarMappable(cmap='PRGn', norm=norm)
im = ax[1].imshow(state2, cmap='PRGn', norm=norm)
cbar = plt.colorbar(sm, ax=ax[1])
cbar.set_label("Spin value")

ax[1].set_title(f"Initial state: T={T2}")
ax[1].set_xticks([])
ax[1].set_yticks([])
plt.tight_layout()
plt.savefig("./IsingModel/Images/expanded-state.png", dpi=500)
plt.show()
