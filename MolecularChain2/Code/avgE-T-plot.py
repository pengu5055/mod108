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
save_path = "./MolecularChain2/Results/avgE-vs-T.h5"
bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)
T_values = np.loadtxt("./MolecularChain2/Code/T_range.lst")
runs = np.arange(1, 101)  # Fish is 1-indexed for some reason

# Containers for data
steps_to_convergence = []
end_energy = []
# Load data
with h5py.File(save_path, "r") as f:
    num_runs = len(f.keys())

    for T in T_values:
        row_steps = []
        row_end_energy = []
        for run in runs:
            key = f"{T}-{run}"
            group = f[key]
            row_steps.append(len(group[f"energy-{key}"]))
            row_end_energy.append(group[f"energy-{key}"][-1])

        steps_to_convergence.append(row_steps)  
        end_energy.append(row_end_energy)

# Calculate statistics
steps_to_convergence = np.array(steps_to_convergence)
avg_steps = np.mean(steps_to_convergence, axis=0)
delta_steps = np.abs(steps_to_convergence - avg_steps)
sigma_steps = np.std(steps_to_convergence, axis=0)

end_energy = np.array(end_energy)
avg_energy = np.mean(end_energy, axis=0)
delta_energy = end_energy - avg_energy
sigma_energy = np.std(end_energy, axis=0)

# Plot data as 3 subplots
colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]
cm = pl.scientific.sequential.Batlow_7.mpl_colormap
cm = cmr.get_sub_cmap(cm, 0.15, 0.85)


fig, ax = plt.subplots(1, 3, figsize=(12, 5))
