"""
Check HDF5 file. Something looks way off...
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py

init_state = np.load("./IsingModel/Results/random-state.npy")

# Load the file
save_path = "./IsingModel/Results/avgE-vs-T-pool.h5"
with h5py.File(save_path, "r") as f:
    key = list(f.keys())[-1]
    state = f[key][f"state-{key}"][:]


# Debug plots
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].imshow(init_state, cmap="gray")
ax[0].set_title("Initial state")

ax[1].imshow(state, cmap="gray")
ax[1].set_title("Final state")

plt.suptitle(f"Init. vs Final for T={float(key):.2e}")

plt.show()



