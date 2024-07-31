"""
Test file for the Ising Model
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolistwo import Metropolis2
import matplotlib as mpl

plt.style.use('./ma-style.mplstyle')
mpl.use("qtagg")


dim = 500
m = Metropolis2((dim, dim), 2.269185)
m.EPS = 10
m.MAX_ITER = int(1e7)
m.ANNEAL_RATE = 1
m.J = -1
s_init, s_final, energies = m.run()


fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].imshow(s_init, cmap='gray')
ax[0].set_title("Initial state")
ax[0].set_xticks([])
ax[0].set_yticks([])

ax[1].imshow(s_final, cmap='gray')
ax[1].set_title("Final state")
ax[1].set_xticks([])
ax[1].set_yticks([])

plt.suptitle(f"Ising: ${dim}^2$ spins, T = ${m.temperatures[0]:.2f}$, ${m.MAX_ITER:.2e}$ iterations")
plt.tight_layout()
plt.savefig("./IsingModel/Images/ising-anti-critical", dpi=500)
plt.show()
