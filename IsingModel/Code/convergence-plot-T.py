import numpy as np
import matplotlib as mpl
import h5py
import cmasher as cmr
import palettable as pl

import matplotlib.pyplot as plt

# Enable custom stylesheet
plt.style.use('./ma-style.mplstyle')
mpl.use("qtagg")

# Simulation parameters
save_path = "./IsingModel/Results/avgE-vs-T-v3.h5"
T_values = np.loadtxt("./IsingModel/Code/T_range.lst")

# Containers for data
steps_to_convergence = []
end_energy = []
end_temperature = []
to_delete = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = 100

    for i, T in enumerate(T_values):
        row_steps = []
        row_end_energy = []
        row_end_temperature = []

        for run in range(num_runs):
            key = f"{T}-{run}"
            group = f[key]
            row_steps.append(len(group[f"energy-{key}"]))
            row_end_energy.append(group[f"energy-{key}"][-1])
            row_end_temperature.append(group[f"temperature-{key}"][-1])

        steps_to_convergence.append(row_steps)  
        end_energy.append(row_end_energy)
        end_temperature.append(row_end_temperature)

# Calculate statistics
steps_to_convergence = np.array(steps_to_convergence)
avg_steps = np.mean(steps_to_convergence, axis=1)
sigma_steps = np.std(steps_to_convergence, axis=1)

# Plot data as 3 subplots
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Average steps to convergence vs. temperature
ax[0].plot(T_values, avg_steps, color=colors[1], alpha=1, lw=3, label="Average Steps")
ax[0].plot(T_values, avg_steps - sigma_steps, color=colors[0], alpha=1, ls="--")
ax[0].plot(T_values, avg_steps + sigma_steps, color=colors[0], alpha=1, ls="--")
ax[0].fill_between(T_values, avg_steps - sigma_steps, avg_steps + sigma_steps,                
                   color=colors[3], alpha=0.3, label="1-$\sigma$ Band")
ax[0].axvline(2.27, color=colors[4], linestyle='--', label=r"$T_{\mathrm{crit}}$")
ax[0].legend(frameon=False)
ax[0].set_ylabel("Average Steps to Convergence")
ax[0].set_xlabel("Temperature")
ax[0].set_title(r"Avg. Steps to Convergence Over $100$ Runs")

# Steps to Convergence vs. Temperature vs. Run
cm = cmr.get_sub_cmap('cmr.bubblegum', 0., 1.)
norm = mpl.colors.LogNorm(vmin=steps_to_convergence.min(), vmax=steps_to_convergence.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)

ax[1].imshow(steps_to_convergence.T, aspect="auto", cmap=cm, norm=norm,
                extent=[T_values[0], T_values[-1], 1, 100])
cbar = plt.colorbar(sm, ax=ax[1])
cbar.set_label("Steps")
ax[1].set_ylabel("Run")
ax[1].set_xlabel("Temperature")
ax[1].set_title("Steps Spread Across Runs")  
cbar.set_ticks([steps_to_convergence.min(), 10000, 20000, 40000, 60000, 80000, steps_to_convergence.max()])
cbar.set_ticklabels([steps_to_convergence.min(), "10000",  "20000", "40000", "60000", "80000", steps_to_convergence.max()])
plt.tight_layout()
plt.savefig("./IsingModel/Images/steps-vs-T.png", dpi=500)
plt.show()