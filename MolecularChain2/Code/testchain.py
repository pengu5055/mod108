"""
Try new implementation.
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolisone import Metropolis1

bounds = (-18, 0)
length = 17
temperature = 10
val = -10
init = np.array([0, val, val, val, val, val, val, val + 5, val, val, val, val, val, val, val, val, 0])
# init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]

m = Metropolis1(length, temperature, bounds, states=init)
m.EXIT_COND2 = True
s_init, s_final, en = m.run()
fig, ax = plt.subplots(1, 3, figsize=(10, 5))

ax[0].plot(s_init, color='blue')
ax[0].plot(s_final, color='red')

ax[1].plot(en, color='blue')

ax[2].plot(m.temperatures, color='green')

plt.tight_layout()
plt.show()
