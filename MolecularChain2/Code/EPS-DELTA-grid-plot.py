"""
Plot results of Temperature vs. Annealing Rate for fixed initial state
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
save_path = "./MolecularChain2/Results/par-gridscan-EPS-DELTA-v2.h5"
bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)
EPS_values = np.loadtxt("./MolecularChain2/Code/EPS_range.lst")
DELTA_values = np.loadtxt("./MolecularChain2/Code/DELTA_range.lst")

# Containers for data
steps_to_convergence = []
end_energy = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = len(f.keys())
    runs = np.arange(0, num_runs)

    for E in EPS_values:
        row_steps = []
        row_end_energy = []
        for D in DELTA_values:
            key = f"{E}-{int(D)}"
            group = f[key]
            row_steps.append(len(group[f"energy-{key}"]))
            row_end_energy.append(group[f"energy-{key}"][-1])

        steps_to_convergence.append(row_steps)  
        end_energy.append(row_end_energy)

# Calculate statistics
steps_to_convergence = np.array(steps_to_convergence)
avg_steps = np.mean(steps_to_convergence)
delta_steps = np.abs(steps_to_convergence - avg_steps)

end_energy = np.array(end_energy)
avg_energy = np.mean(end_energy)
delta_energy = end_energy - avg_energy

# Plot data as 2 heatmaps
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]
cm = pl.scientific.sequential.Batlow_7.mpl_colormap
cm = cmr.get_sub_cmap(cm, 0.15, 0.85)


fig, ax = plt.subplots(1, 2, figsize=(12, 5))
print(EPS_values)
# EPS_values = np.log10(EPS_values)
# norm = mpl.colors.PowerNorm(gamma=0.2, vmin=delta_steps.min(), vmax=delta_steps.max())
norm = mpl.colors.Normalize(vmin=delta_steps.min(), vmax=delta_steps.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)

ax[0].imshow(delta_steps, cmap=cm, aspect="auto", norm=norm,
             extent=[DELTA_values[0], DELTA_values[-1], EPS_values[-1], EPS_values[0]])
cbar = plt.colorbar(sm, ax=ax[0])
# cbar.set_ticks(np.logspace(np.log10(delta_steps.min()), np.log10(delta_steps.max()), 10))
avg_steps_text = f"Avg. Steps: {avg_steps:.2f}"
ax[0].text(0.05, 0.95, avg_steps_text, transform=ax[0].transAxes,
           fontsize=12, verticalalignment='top', horizontalalignment='left',
           color='white', bbox=dict(facecolor='black', alpha=0.2, edgecolor='black', boxstyle='round,pad=0.5'))
ax[0].set_xlabel(r"State Change at Move $\Delta$")
ax[0].set_ylabel(r"Tolerance $\varepsilon$")
ax[0].set_xticks(DELTA_values)
#ax[0].set_yticks(EPS_values)
ax[0].set_title("Deviation from Avg. Steps to Convergence")


# Plot 2
cm = pl.scientific.diverging.Berlin_3.mpl_colormap
cm = cmr.get_sub_cmap(cm, 0.15, 0.85, N=len(range(int(delta_energy.min()), int(delta_energy.max()))))
# norm = mpl.colors.TwoSlopeNorm(vmin=delta_energy.min(), vmax=delta_energy.max(), vcenter=0)
norm = mpl.colors.Normalize(vmin=delta_energy.min(), vmax=delta_energy.max())
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)

ax[1].imshow(delta_energy, cmap=cm, aspect="auto", norm=norm,
                extent=[DELTA_values[0], DELTA_values[-1], EPS_values[-1], EPS_values[0]])
cbar = plt.colorbar(sm, ax=ax[1])
manual_ticks = np.array([delta_energy.min(), -20, -10, 0, 100, 500, 750, delta_energy.max()])
# cbar.set_ticks(manual_ticks)
avg_steps_text = f"Avg. End Energy: {avg_energy:.2f}$"
ax[1].text(0.05, 0.95, avg_steps_text, transform=ax[1].transAxes,
           fontsize=12, verticalalignment='top', horizontalalignment='left',
           color='white', bbox=dict(facecolor='black', alpha=0.2, edgecolor='black', boxstyle='round,pad=0.5'))

ax[1].set_xlabel(r"State Change at Move $\Delta$")
ax[1].set_ylabel(r"Tolerance $\varepsilon$")
ax[1].set_xticks(DELTA_values)
ax[1].set_yticks(np.logspace(np.log10(EPS_values[-1]), np.log10(EPS_values[0]), num=10))
ax[1].set_title("Deviation from Avg. Final Energy")

plt.savefig("./MolecularChain2/Images/EPS-DELTA-gridscan.png", dpi=400)
plt.tight_layout()
plt.show()
