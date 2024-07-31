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
m = Metropolis2((100, 100), 2.27)
m.EPS = 10
m.state_bounds = (-4, 4)
m.MAX_ITER = int(1e8)
m.ANNEAL_RATE = 1
state1, state2, energies = m.run()


cm = pl.colorbrewer.diverging.Spectral_11.mpl_colors
cm = mpl.colors.LinearSegmentedColormap.from_list("temps", cm, N=9)
sm = plt.cm.ScalarMappable(cmap=cm, norm=mpl.colors.Normalize(vmin=-4, vmax=4))

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

norm = mpl.colors.Normalize(vmin=-2, vmax=2)
im = ax[0].imshow(state1, cmap=cm, norm=norm, aspect='auto')
cbar = plt.colorbar(sm, ax=ax[0], ticks=(np.arange(-4, 5, 1) * 8/9))
cbar.set_label("Spin value")
cbar.ax.axes.tick_params(length=0)
cbar.set_ticklabels(np.arange(-4, 5, 1))

ax[0].set_title(f"Initial State")
ax[0].set_xticks([])
ax[0].set_yticks([])

# Final state
im = ax[1].imshow(state2, cmap=cm, norm=norm, aspect='auto')
cbar = plt.colorbar(sm, ax=ax[1], ticks=(np.arange(-4, 5, 1) * 8/9))
cbar.set_label("Spin value")
cbar.ax.axes.tick_params(length=0)
cbar.set_ticklabels(np.arange(-4, 5, 1))

ax[1].set_title(f"Final State")
ax[1].set_xticks([])
ax[1].set_yticks([])

plt.tight_layout()
plt.savefig("./IsingModel/Images/expanded-xlong-state-critical.png", dpi=500)
plt.show()
