"""
Test in-development code here.
"""
import numpy as np
import matplotlib.pyplot as plt
from simcityone import SimCity_1D
import palettable as pl
import cmasher as cmr

cm = pl.colorbrewer.sequential.PuRd_7.mpl_colormap
colors = cmr.take_cmap_colors(cm, 7, cmap_range=(0.1, 0.9), return_fmt='hex')

init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
print(isinstance(init, list | tuple | np.ndarray))
print(len(init))
sc = SimCity_1D(17, 1, (-18, 0), states=init)
sc2 = SimCity_1D(17, 1, (-18, 0))
sc3 = SimCity_1D(17, 1, (-18, 0))

N = int(10e6)

pre_state = np.copy(sc.state)
pre_state2 = np.copy(sc2.state)
pre_state3 = np.copy(sc3.state)
states, energies = sc.run(N)
states2, energies2 = sc2.run(N)
states3, energies3 = sc3.run(N)


fig, ax = plt.subplots(1, 2, figsize=(10, 5))

colors2 = cmr.take_cmap_colors(pl.cartocolors.sequential.DarkMint_7.mpl_colormap,
                               7, cmap_range=(0.1, 0.9), return_fmt='hex')
colors3 = cmr.take_cmap_colors(pl.cartocolors.sequential.PurpOr_7.mpl_colormap,
                                 7, cmap_range=(0.1, 0.9), return_fmt='hex')

ax[0].plot(states, color=colors[4])
ax[0].plot(pre_state, ls="--", color=colors[1])
ax[0].plot(states2, color=colors2[4])
ax[0].plot(pre_state2, ls="--", color=colors2[1])
ax[0].plot(states3, color=colors3[4])
ax[0].plot(pre_state3, ls="--", color=colors3[1])
ax[0].legend(["Final State", "Initial State"])



ax[1].plot(energies, color=colors[4])
ax[1].plot(energies2, color=colors2[4])
ax[1].plot(energies3, color=colors3[4])

# Add textbox with final energies
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = f"Final Energy: {energies[-1]:.2f}\nFinal Energy: {energies2[-1]:.2f}\nFinal Energy: {energies3[-1]:.2f}"
ax[1].text(0.45, 0.95, textstr, transform=ax[1].transAxes, fontsize=10,
           verticalalignment='top', bbox=props)



plt.show()
