"""
Plot the average relaxation energy of the system as a function of temperature.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import palettable as pl
from metropolistwoexpanded import Metropolis2

# Enable custom stylesheet
plt.style.use('./ma-style.mplstyle')
mpl.use("qtagg")

# Simulation parameters
m = Metropolis2((500, 500), 10)
m.EPS = 10
m.state_bounds = (-2, 2)
m.MAX_ITER = int(2*1e7)
m.ANNEAL_RATE = 1
state1, state2, energies = m.run()


cm = pl.cartocolors.diverging.Temps_5.mpl_colors
cm = mpl.colors.LinearSegmentedColormap.from_list("temps", cm, N=5)
sm = plt.cm.ScalarMappable(cmap=cm, norm=mpl.colors.Normalize(vmin=-2, vmax=2))

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

norm = mpl.colors.Normalize(vmin=-2, vmax=2)
im = ax[0].imshow(state1, cmap=cm, norm=norm, aspect='auto')
cbar = plt.colorbar(sm, ax=ax[0], ticks=[-1.6, -0.8, 0, 0.8, 1.6])
cbar.set_label("Spin value")
cbar.ax.axes.tick_params(length=0)
cbar.set_ticklabels(['-2', '-1', '0', '1', '2'])

ax[0].set_title(f"Initial State")
ax[0].set_xticks([])
ax[0].set_yticks([])

# Final state
im = ax[1].imshow(state2, cmap=cm, norm=norm, aspect='auto')
cbar = plt.colorbar(sm, ax=ax[1], ticks=[-1.6, -0.8, 0, 0.8, 1.6])
cbar.set_label("Spin value")
cbar.ax.axes.tick_params(length=0)
cbar.set_ticklabels(['-2', '-1', '0', '1', '2'])

ax[1].set_title(f"Final State")
ax[1].set_xticks([])
ax[1].set_yticks([])

plt.tight_layout()
plt.savefig("./IsingModel/Images/expanded-state-supercritical.png", dpi=500)
plt.show()
