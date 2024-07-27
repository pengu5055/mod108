"""
Test file for the Ising Model
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolistwo import Metropolis2

m = Metropolis2((100, 100), 1)

fig, ax = plt.subplots()
ax.imshow(m.states, cmap='gray')

plt.tight_layout()
plt.show()
