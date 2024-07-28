"""
Test file for the Ising Model
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolistwo import Metropolis2

m = Metropolis2((100, 100), 1)
s_init, s_final, energies = m.run()


fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].imshow(s_init, cmap='gray')
ax[0].set_title("Initial state")
ax[0].axis('off')

ax[1].imshow(s_final, cmap='gray')
ax[1].set_title("Final state")
ax[1].axis('off')

plt.tight_layout()
plt.savefig("./IsingModel/Images/isingmodel.png", dpi=400)
plt.show()
