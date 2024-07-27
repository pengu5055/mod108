"""
A script where we change the rules of the system a bit and see how the chain shape changes.
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolisone import Metropolis1
import h5py
from sys import argv

# Use custom stylesheet
plt.style.use('./ma-style.mplstyle')

bounds = (-50, 0)
length = 25
temperature = 1
molecules = np.arange(0, length)

m = Metropolis1(length, temperature, bounds)
m.EXIT_COND2 = False
m.STOP_STEPS = 50
m.EPS = 1e-14
s_init, s_final, en = m.run()

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