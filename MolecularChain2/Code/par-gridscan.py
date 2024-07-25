"""
Perform a grid scan of the parameter space for the molecular chain model, where 
by parameters I mean the various conditions that can be set for the Metropolis
algorithm.
Usage:

    python ./MolecularChain2/Code/par-gridscan.py $TEMPERATURE $ANNEAL_RATE
"""
import numpy as np
import matplotlib.pyplot as plt
from metropolisone import Metropolis1
import h5py
from sys import argv


bounds = (-18, 0)
length = 17
temperature = argv[1]
init = [0, -17, -4, -2, -8, -13, -7, -2, -5, -2, -3, -2, -3, -10, -15, -7, 0]
molecules = np.arange(0, 17)

m = Metropolis1(length, temperature, bounds, states=init)
m.EXIT_COND2 = False
m.STOP_STEPS = 50
m.EPS = 1e-14
m.ANNEAL_RATE = argv[2]
s_init, s_final, en = m.run()

if True:
    save_path = "./MolecularChain2/Results/par-gridscan-T-annealR.h5"
    T_number = argv[1]
    anneal_number = argv[2]
    print(f"Storing run {T_number, anneal_number} to '{save_path}'..")

    with h5py.File(save_path, "a") as f:
        group = f.create_group(f"{T_number}-{anneal_number}")
        dset_state = group.create_dataset(f"state-{T_number}-{anneal_number}", data=s_final)
        dset_en = group.create_dataset(f"energy-{T_number}-{anneal_number}", data=en)
        dset_t = group.create_dataset(f"temperature-{T_number}-{anneal_number}", data=m.temperatures)

    print(f"Saved!")
