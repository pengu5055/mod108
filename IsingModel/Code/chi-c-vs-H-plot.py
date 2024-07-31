"""
Plot spin susceptibility and heat capacity as a function of magnetic field.
"""
import numpy as np
import matplotlib.pyplot as plt

# Calculate Observables: Eigenmagnetization
def magnetization(state: np.ndarray):
    S = np.array([np.sum(np.array(final)) for final in state]) 
    return S


# Load data
S = np.load("./IsingModel/Results/S-v2.npy")
energies = np.load("./IsingModel/Results/E-v2.npy")
H_values = np.loadtxt("./IsingModel/Code/H_range.lst")
