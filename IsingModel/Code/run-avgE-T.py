"""
With approx 5 min per run and 100 temperatures, this would take 500 minutes, or 8 hours and 20 minutes.
I'm sorta on my old shit again.
"""
import numpy as np
import concurrent.futures
from metropolistwo import Metropolis2
import h5py

class Worker:
    def __init__(self,
                 temperature: float,
                 ):
        self.T = temperature
    
    def process(self):
        dim = (500, 500)
        m = Metropolis2(dim, self.T)
        # Contrary to the silly name I chose this is not a random state, but a fixed one
        # The fixed state was created randomly in the create-fixed-init.py script, hence the name
        m.state = np.load("./IsingModel/Results/random-state.npy")
        m.MAX_ITER = 1e7
        m.quiet = True
        print(f"[INFO] Starting: T={self.T}")
        s_init, s_final, en = m.run()

        return s_init, s_final, en, m.temperatures
    
# Create function that'll get the workders to work
def worker_task(params):
    worker = Worker(*params)
    return worker.process()
    
# Get Thread Pool parameter list
param_list = np.genfromtxt("./IsingModel/Code/T_range.lst")
param_list = [[par] for par in param_list]

# Run process pool and save on thread execution
with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = [executor.submit(worker_task, params) for params in param_list]
    
    # Step 4: Collect the results
    for future in concurrent.futures.as_completed(futures):
        s_init, s_final, en, temps = future.result()
        arg1 = temps[0]
        
        save_path = "./IsingModel/Results/avgE-vs-T-pool.h5"
        print(f"Storing run {arg1} to '{save_path}'..")

        with h5py.File(save_path, "a") as f:
            group = f.create_group(f"{arg1}")
            dset_state = group.create_dataset(f"state-{arg1}", data=s_final)
            dset_en = group.create_dataset(f"energy-{arg1}", data=en)
            dset_t = group.create_dataset(f"temperature-{arg1}", data=temps)
        print(f"Saved!")
