"""
Test in-development code here.
"""
import numpy as np
import matplotlib.pyplot as plt
from simcityone import SimCity_1D

sc = SimCity_1D(100, 1, (-18, 0))

plt.plot(sc.state)
plt.show()