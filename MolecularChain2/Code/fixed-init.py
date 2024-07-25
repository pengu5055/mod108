"""
This file runs the Metropolis-Hastings algorithm with a fixed initial configuration of the 
molecular chain. This is to gauge the convergence of the algorithm with a fixed initial conditions.
Usage:

    python ./MolecularChain2/Code/fixed-init.py $ITER
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolisone import Metropolis1
import h5py
from sys import argv

# Use custom stylesheet
plt.style.use('./ma-style.mplstyle')

bounds = (-18, 0)
length = 17
temperature = 1
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)

m = Metropolis1(length, temperature, bounds, states=init)
m.EXIT_COND2 = False
m.STOP_STEPS = 50
m.EPS = 1e-14
s_init, s_final, en = m.run()

# Append the run to HDF5
if False:
    save_path = "./MolecularChain2/Results/fixed-initial.h5"
    iter_number = argv[1]
    print(f"Storing run {iter_number} to '{save_path}'..")

    with h5py.File(save_path, "a") as f:
        group = f.create_group(f"{iter_number}")
        dset_state = group.create_dataset(f"state-{iter_number}", data=s_final)
        dset_en = group.create_dataset(f"energy-{iter_number}", data=en)
        dset_t = group.create_dataset(f"temperature-{iter_number}", data=m.temperatures)

    print(f"Saved!")

# Plotting
if True:
    colors = ["#37123c","#d72483","#ddc4dd","#60afff","#98CE00"]

    fig, ax = plt.subplots(1, 3, figsize=(10, 5))

    ax[0].plot(s_init, color=colors[2], zorder=1)
    ax[0].scatter(molecules, s_init, color=colors[1], alpha=0.3, s=15, zorder=2)
    ax[0].plot(s_final, color=colors[1], zorder=1)
    ax[0].scatter(molecules, s_final, color=colors[0], alpha=1, s=15, zorder=2)
    ax[0].set_xlabel("Molecule in Chain")
    ax[0].set_ylabel("State")
    ax[0].set_title("State Evolution")

    ax[1].plot(en, color=colors[3])
    ax[1].set_xlabel("Iteration")
    ax[1].set_ylabel("Energy [arb. units]")

    ax[1].set_title("Energy Minimization")

    ax[2].plot(m.temperatures, color=colors[4])
    ax[2].set_xlabel("Iteration")
    ax[2].set_ylabel("Temperature [arb. units]")
    ax[2].set_title("Temperature Annealing")

    plt.tight_layout()
    plt.savefig("fixed-init.png", dpi=400)
    plt.show()