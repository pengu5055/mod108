"""
Use the data gathered to calculate the average shape of the chain at the end for a fixed temperature.
Maybe try and plot the change in the chain shape as a function of the temperature.
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
save_path = "./MolecularChain2/Results/avgE-vs-T.h5"
bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)
T_values = np.loadtxt("./MolecularChain2/Code/T_range.lst")
runs = np.arange(1, 101)  # Fish is 1-indexed for some reason

# Containers for data
shapes = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = len(f.keys())

    for T in T_values:
        row_shapes = []
        for run in runs:
            key = f"{T}-{run}"
            group = f[key]
            row_shapes.append(group[f"state-{key}"][:])

        shapes.append(row_shapes)   

# Calculate statistics
shapes = np.array(shapes)
avg_shape = np.mean(shapes, axis=1)
sigma_shape = np.std(shapes - avg_shape, axis=1)
avg_avg_shape = np.mean(avg_shape, axis=0)
avg_sigma = np.std(avg_shape - avg_avg_shape, axis=0)


# Plot average shape
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(molecules, avg_avg_shape, color=colors[1], alpha=0.8, label="Average Shape across all T")
ax[0].errorbar(molecules, avg_avg_shape, yerr=avg_sigma, linestyle='None',
               color=colors[0], label=r"1-$\sigma$ error", fmt='o', capsize=5)
ax[0].set_xlabel("Molecule")
ax[0].set_ylabel("State")
ax[0].legend(frameon=False)
ax[0].set_title(r"Average Shape of Chain across all $T$")


# Plot average shape for each T
colors2 = cmr.take_cmap_colors("cmr.bubblegum", len(T_values))
norm = mpl.colors.Normalize(vmin=T_values.min(), vmax=T_values.max())
sm = plt.cm.ScalarMappable(cmap=cmr.bubblegum, norm=norm)

for i, T in enumerate(T_values):
    ax[1].plot(molecules, avg_shape[i], color=colors2[i], alpha=0.5, zorder=(100-i))

cbar = fig.colorbar(sm, ax=ax[1])
cbar.set_label("Temperature")
ax[1].set_xlabel("Molecule")
ax[1].set_ylabel("State")
ax[1].set_title(r"Average Shape of Chain across all $T$")

plt.tight_layout()
plt.savefig("./MolecularChain2/Images/rand-init-T-spread.png", dpi=400)
plt.show()


