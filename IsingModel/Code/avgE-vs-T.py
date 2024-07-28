"""
Calculate the average energy of the system as a function of temperature, given 
a fixed number of steps.
Usage:

    python ./IsingModel/Code/avgE-vs-T.py $TEMPERATURE
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolistwo import Metropolis2
import h5py
from sys import argv
from time import time


dim = (500, 500)
temperature = float(argv[1])

m = Metropolis2(dim, temperature)
# Contrary to the silly name I chose this is not a random state, but a fixed one
# The fixed state was created randomly in the create-fixed-init.py script, hence the name
m.state = np.load("./IsingModel/Results/random-state.npy")
m.MAX_ITER = 1e7

t_start = time()
s_init, s_final, en = m.run()
t_end = time() - t_start

if True:
    save_path = "./IsingModel/Results/avgE-vs-T-v2.h5"
    arg1 = argv[1]  # Temperature
    print(f"Storing run {arg1} to '{save_path}'..")

    with h5py.File(save_path, "a") as f:
        group = f.create_group(f"{arg1}")
        dset_state = group.create_dataset(f"state-{arg1}", data=s_final)
        dset_en = group.create_dataset(f"energy-{arg1}", data=en)
        dset_t = group.create_dataset(f"temperature-{arg1}", data=m.temperatures)

    print(f"Saved!")
    print(f"Elapsed time: {t_end:.2f} seconds")