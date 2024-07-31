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
save_path = "./IsingModel/Results/avgE-vs-T-expanded.h5"
T_values = np.loadtxt("./IsingModel/Code/T_range.lst")

# Containers for data
steps_to_convergence = []
end_energy = []
end_temperature = []
end_states = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = 10

    for i, T in enumerate(T_values):
        row_states = []
        row_steps = []
        row_end_energy = []
        row_end_temperature = []

        for run in range(num_runs):
            key = f"{T}-{run}"
            group = f[key]
            row_states.append(group[f"state-{key}"][:])
            row_steps.append(len(group[f"energy-{key}"]))
            row_end_energy.append(group[f"energy-{key}"][-1])
            row_end_temperature.append(group[f"temperature-{key}"][-1])

        end_states.append(row_states)
        steps_to_convergence.append(row_steps)  
        end_energy.append(row_end_energy)
        end_temperature.append(row_end_temperature)

# Calculate statistics
end_energy = np.array(end_energy)
avg_energy = np.mean(end_energy, axis=1)
sigma_energy = np.std(end_energy, axis=1)

# Calculate Observables: Eigenmagnetization
def magnetization(state: np.ndarray):
    S = np.array([[np.sum(np.array(final[run])) for run in range(num_runs)] for final in end_states]) 
    return S

S = np.abs(magnetization(end_states))
avgS = np.mean(S, axis=1)
sigmaS = np.std(S, axis=1)

crit_T = 2.27

# Plot data as 3 subplots
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]

fig, ax = plt.subplots(2, 2, figsize=(12, 9))

# Average energy vs. temperature
ax[0, 0].plot(T_values, avg_energy, color=colors[1], alpha=1, lw=3, label="Average Energy")
ax[0, 0].plot(T_values, avg_energy - sigma_energy, color=colors[0], alpha=1, ls="--")
ax[0, 0].plot(T_values, avg_energy + sigma_energy, color=colors[0], alpha=1, ls="--")
ax[0, 0].fill_between(T_values, avg_energy - sigma_energy, avg_energy + sigma_energy, 
                      color=colors[3], alpha=0.3, label="1-$\sigma$ Band")

ax[0, 0].axvline(crit_T, color=colors[4], linestyle='--', label=r"$T_{\mathrm{crit}}$")
ax[0, 0].legend(frameon=False)
ax[0, 0].set_ylabel("Average Energy [arb. units]")
ax[0, 0].set_xlabel("Temperature")
ax[0, 0].set_title(r"Avg. Final Energy For Expanded States")


# Average magnetization vs. temperature
ax[0, 1].plot(T_values, avgS, color=colors[1], alpha=1, lw=3, label="Average Magnetization")
ax[0, 1].plot(T_values, avgS - sigmaS, color=colors[0], alpha=1, ls="--")
ax[0, 1].plot(T_values, avgS + sigmaS, color=colors[0], alpha=1, ls="--")
ax[0, 1].fill_between(T_values, avgS - sigmaS, avgS + sigmaS, 
                      color=colors[3], alpha=0.3, label="1-$\sigma$ Band")

ax[0, 1].axvline(crit_T, color=colors[4], linestyle='--', label=r"$T_{\mathrm{crit}}$")
ax[0, 1].legend(frameon=False)
ax[0, 1].set_ylabel("|Average Magnetization| [arb. units]")
ax[0, 1].set_xlabel("Temperature")
ax[0, 1].set_title(r"|Avg. Magnetization| For Expanded States")

# End Energy vs. Temperature vs. Run
cm = cmr.get_sub_cmap('cmr.bubblegum', 0., 1.)
norm = mpl.colors.Normalize(vmin=end_energy.min(), vmax=end_energy.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
ax[1, 0].imshow(end_energy.T, aspect="auto", cmap=cm, norm=norm,
                extent=[T_values[0], T_values[-1], 100, 1])
cbar = plt.colorbar(sm, ax=ax[1, 0])
cbar.set_label("Energy [arb. units]")
ax[1, 0].set_ylabel("Run")
ax[1, 0].set_xlabel("Temperature")
ax[1, 0].set_title("Final Energy Spread Across Runs")
ax[1, 0].set_yticks(np.arange(10, 110, 10))
ax[1, 0].set_yticklabels(np.arange(1, 11)) 


# Steps to Convergence vs. Temperature vs. Run
cm = cmr.get_sub_cmap('cmr.bubblegum', 0., 1.)
norm = mpl.colors.Normalize(vmin=S.min(), vmax=S.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)

ax[1, 1].imshow(S.T, aspect="auto", cmap=cm, norm=norm,
                extent=[T_values[0], T_values[-1], 100, 1])
cbar = plt.colorbar(sm, ax=ax[1, 1])
cbar.set_label("|Magnetization| [arb. units]")
# cbar.set_ticks([steps_to_convergence.min(), 1000, 10000, steps_to_convergence.max()])
# cbar.set_ticklabels([steps_to_convergence.min(), "1000", "10000", steps_to_convergence.max()])
ax[1, 1].set_ylabel("Run")
ax[1, 1].set_xlabel("Temperature")
ax[1, 1].set_title("|Magnetizaion| Spread Across Runs") 
ax[1, 1].set_yticks(np.arange(10, 110, 10))
ax[1, 1].set_yticklabels(np.arange(1, 11)) 


plt.tight_layout()
plt.savefig("./IsingModel/Images/avgE-avgS-vs-T-expanded.png", dpi=500)
plt.show()
