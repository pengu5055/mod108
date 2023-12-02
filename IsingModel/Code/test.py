"""
Test in-development code here.
"""
import numpy as np
import matplotlib.pyplot as plt
from simcitytwo import SimCity_2D
import palettable as pl
import cmasher as cmr

cm = pl.scientific.sequential.GrayC_20.mpl_colormap
colors = cmr.take_cmap_colors(cm, 7, cmap_range=(0.1, 0.9), return_fmt='hex')

M = 100
temperature = 273
bounds = (0, 1)

sc = SimCity_2D(M, temperature, bounds)

N = int(10e5)

pre_state = np.copy(sc.state)
states, energies = sc.run(N)

fig, ax = plt.subplots(1, 2, figsize=(10, 5))

norm = plt.Normalize(vmin=bounds[0], vmax=bounds[1])

ax[0].imshow(pre_state, cmap=cm, norm=norm)
ax[1].imshow(states, cmap=cm, norm=norm)

plt.show()

# NOTE: Current code makes rows look significant which is 
# very odd. Need to fix this.
