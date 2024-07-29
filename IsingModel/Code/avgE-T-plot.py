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
save_path = "./IsingModel/Results/avgE-vs-T-pool.h5"
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
to_delete = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = len(f.keys())

    for i, T in enumerate(T_values):
        row_steps = []
        row_end_energy = []
        row_end_temperature = []
        key = f"{T}"
        try:
            group = f[key]
        except KeyError:
            print(f"Missing data: {key}")
            to_delete.append(i)
            continue
        row_steps.append(len(group[f"energy-{key}"]))
        row_end_energy.append(group[f"energy-{key}"][-1])
        row_end_temperature.append(group[f"temperature-{key}"][-1])

        steps_to_convergence.append(row_steps)  
        end_energy.append(row_end_energy)
        end_temperature.append(row_end_temperature)

# Remove missing data
T_values = np.delete(T_values, to_delete)

# Calculate statistics
steps_to_convergence = np.array(steps_to_convergence)
avg_steps = np.mean(steps_to_convergence, axis=1)
sigma_steps = np.std(steps_to_convergence - avg_steps, axis=1)

end_energy = np.array(end_energy)
avg_energy = np.mean(end_energy, axis=1)
sigma_energy = np.std(end_energy, axis=1)

end_temperature = np.array(end_temperature)
avg_temperature = np.mean(end_temperature, axis=1)
delta_temp = T_values - avg_temperature
sigma_temperature = np.std(T_values - end_temperature, axis=1)

# Plot data as 3 subplots
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]

fig, ax = plt.subplots(2, 2, figsize=(12, 9))

# Average energy vs. temperature
ax[0, 0].plot(T_values, avg_energy, color=colors[1], alpha=1, lw=3, label="Average Energy")
ax[0, 0].plot(T_values, avg_energy - sigma_energy, color=colors[0], alpha=1, ls="--")
ax[0, 0].plot(T_values, avg_energy + sigma_energy, color=colors[0], alpha=1, ls="--")
ax[0, 0].fill_between(T_values, avg_energy - sigma_energy, avg_energy + sigma_energy, color=colors[3], alpha=0.3)


ax[0, 0].set_xscale("log")
ax[0, 0].set_ylabel("Average Energy")
ax[0, 0].set_xlabel("Temperature")
ax[0, 0].set_title(r"Avg. Final Energy Over $100$ Runs")


# Average steps to convergence vs. temperature
ax[0, 1].plot(T_values, avg_steps, color=colors[1], alpha=1, lw=3, label="Average Energy")
ax[0, 1].plot(T_values, avg_steps - sigma_steps, color=colors[0], alpha=1, ls="--")
ax[0, 1].plot(T_values, avg_steps + sigma_steps, color=colors[0], alpha=1, ls="--")
ax[0, 1].fill_between(T_values, avg_steps - sigma_steps, avg_steps + sigma_steps, color=colors[3], alpha=0.3)

ax[0, 1].set_xscale("log")
ax[0, 1].set_ylabel("Average Steps to Convergence")
ax[0, 1].set_xlabel("Temperature")
ax[0, 1].set_title(r"Avg. Steps to Convergence Over $100$ Runs")

# End Energy vs. Temperature vs. Run
cm = cmr.get_sub_cmap('cmr.bubblegum', 0., 1.)
norm = mpl.colors.Normalize(vmin=end_energy.min(), vmax=end_energy.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
ax[1, 0].imshow(end_energy.T, aspect="auto", cmap=cm, norm=norm,
                extent=[T_values[0], T_values[-1], 100, 1])
cbar = plt.colorbar(sm, ax=ax[1, 0])
cbar.set_label("Energy")
ax[1, 0].set_ylabel("Run")
ax[1, 0].set_xlabel("Temperature")
ax[1, 0].set_title("Final Energy Spread Across Runs")  

# Steps to Convergence vs. Temperature vs. Run
cm = cmr.get_sub_cmap('cmr.bubblegum', 0., 1.)
norm = mpl.colors.LogNorm(vmin=steps_to_convergence.min(), vmax=steps_to_convergence.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)

ax[1, 1].imshow(steps_to_convergence.T, aspect="auto", cmap=cm, norm=norm,
                extent=[T_values[0], T_values[-1], 1, 100])
cbar = plt.colorbar(sm, ax=ax[1, 1])
cbar.set_label("Steps")
# cbar.set_ticks([steps_to_convergence.min(), 1000, 10000, steps_to_convergence.max()])
# cbar.set_ticklabels([steps_to_convergence.min(), "1000", "10000", steps_to_convergence.max()])
ax[1, 1].set_ylabel("Run")
ax[1, 1].set_xlabel("Temperature")
ax[1, 1].set_title("Steps to Convergence Spread Across Runs")  

plt.tight_layout()
plt.savefig("./IsingModel/Images/avgE-vs-T.png", dpi=500)
plt.show()
