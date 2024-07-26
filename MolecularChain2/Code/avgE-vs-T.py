"""
Calculate the average energy of the system as a function of temperature.
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolisone import Metropolis1
import h5py
from sys import argv


bounds = (-18, 0)
length = 17
temperature = float(argv[1])
molecules = np.arange(0, 17)

m = Metropolis1(length, temperature, bounds)
m.EXIT_COND2 = False
m.STOP_STEPS = 50
m.EPS = 1e-14
s_init, s_final, en = m.run()

if True:
    save_path = "./MolecularChain2/Results/avgE-vs-T-v2.h5"
    arg1 = argv[1]  # Temperature
    arg2 = argv[2]  # Run number
    print(f"Storing run {arg1, arg2} to '{save_path}'..")

    with h5py.File(save_path, "a") as f:
        group = f.create_group(f"{arg1}-{arg2}")
        dset_state = group.create_dataset(f"state-{arg1}-{arg2}", data=s_final)
        dset_en = group.create_dataset(f"energy-{arg1}-{arg2}", data=en)
        dset_t = group.create_dataset(f"temperature-{arg1}-{arg2}", data=m.temperatures)

    print(f"Saved!")