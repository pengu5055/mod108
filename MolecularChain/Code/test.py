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

sc = SimCity_1D(10, 1, (-18, 0))

pre_state = np.copy(sc.state)
plt.plot(pre_state)
plt.show()

states, energies = sc.run(1000)

plt.plot(states, color=colors[4])
plt.plot(pre_state, ls="--", color=colors[1])
plt.show()


sc.state = [-4] * 10
print(sc._energy())