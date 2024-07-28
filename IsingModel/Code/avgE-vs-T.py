"""
Calculate the average energy of the system as a function of temperature, given 
a fixed number of steps.
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolistwo import Metropolis2
import h5py
from sys import argv


dim = (100, 100)
temperature = float(argv[1])
molecules = np.arange(0, 17)

m = Metropolis2(dim, temperature, bounds)

s_init, s_final, en = m.run()

if True:
    save_path = "./IsingModel/Results/avgE-vs-T-v2.h5"
    arg1 = argv[1]  # Temperature
    arg2 = argv[2]  # Run number
    print(f"Storing run {arg1, arg2} to '{save_path}'..")

    with h5py.File(save_path, "a") as f:
        group = f.create_group(f"{arg1}-{arg2}")
        dset_state = group.create_dataset(f"state-{arg1}-{arg2}", data=s_final)
        dset_en = group.create_dataset(f"energy-{arg1}-{arg2}", data=en)
        dset_t = group.create_dataset(f"temperature-{arg1}-{arg2}", data=m.temperatures)

    print(f"Saved!")