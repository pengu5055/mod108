"""
Script to make plots for the multiple runs of the fixed initial conditions.
Data is saved in "./MolecularChain2/Results/fixed-initial.h5"
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import h5py

# Enable custom stylesheet
plt.style.use('./ma-style.mplstyle')

# Simulation parameters
save_path = "./MolecularChain2/Results/fixed-initial.h5"
bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)

# Containers for data
final_state = []
final_energies = []
final_temperature = []

# Load data
with h5py.File(save_path, "r") as f:
    num_runs = len(f.keys())
    runs = np.arange(0, num_runs)

    # Demo usage: load data from first run
    # group_key = list(f.keys())[0]
    # group = f[group_key]
    # state = group["state-0"][:]
    # energy = group["energy-0"][:]
    # temperature = group["temperature-0"][:]

    # Load data from all runs
    for key in list(f.keys()):
        group = f[key]
        final_state.append(group[f"state-{key}"][:])
        final_energies.append(group[f"energy-{key}"][-1])
        final_temperature.append(group[f"temperature-{key}"][-1])


# Calculate statistics
final_state = np.array(final_state)
avg_state = np.mean(final_state, axis=0)
delta_state = final_state - avg_state
sigma_state = np.std(delta_state, axis=0)

final_energies = np.array(final_energies)
avg_energy = np.mean(final_energies)
avg_temperature = np.mean(final_temperature)
delta_energy = final_energies - avg_energy
sigma_energy = np.std(delta_energy)

final_temperature = np.array(final_temperature)
delta_temperature = final_temperature - avg_temperature
sigma_temperature = np.std(delta_temperature)


# Plot data
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]

fig, ax = plt.subplots(1, 3, figsize=(12, 5))

ax[0].plot(init, color=colors[2], zorder=1)
ax[0].scatter(molecules, init, color=colors[1], alpha=0.3, s=15, zorder=2)
ax[0].plot(avg_state, color=colors[1], zorder=1)
ax[0].errorbar(molecules, avg_state, yerr=sigma_state, color=colors[0], alpha=1, fmt='o', markersize=5, capsize=3, zorder=2)
ax[0].set_xlabel("Molecule in Chain")
ax[0].set_ylabel("State")
ax[0].set_title("Average State at Convergence")

ax[1].axhline(avg_energy, color=colors[4], linestyle='--')
ax[1].plot(delta_energy, color=colors[3])
ax[1].scatter(runs, delta_energy, color=colors[0], alpha=1, s=15)
ax[1].set_xlabel("Run")
ax[1].set_ylabel("Energy [arb. units]")
ax[1].set_title("Scatter of Energies")

t_min = final_temperature.min()
t_max = final_temperature.max()
t_range_offset = (t_max - t_min) * 0.15

ax[2].axhline(avg_temperature, color=colors[2], linestyle='--', label=f"Average $T$")
ax[2].scatter(runs, final_temperature, color=colors[1], alpha=1, s=15)
ax[2].axhline(avg_temperature + sigma_temperature, color=colors[0], ls=':')
ax[2].axhline(avg_temperature - sigma_temperature, color=colors[0], ls=':')
ax[2].fill_between(runs, avg_temperature - sigma_temperature, avg_temperature + sigma_temperature,
                   color=colors[3], alpha=0.3, label=r"1-$\sigma$ band")
ax[2].set_ylim(t_min - t_range_offset, t_max + t_range_offset)
ax[2].set_xlim(0, num_runs)

ax[2].set_xlabel("Run")
ax[2].set_ylabel("Temperature [arb. units]")
ax[2].set_title("Scatter of Temperatures")


plt.tight_layout()
plt.savefig("fixed-init-multiple.png", dpi=400)
plt.show()