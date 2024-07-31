"""
With approx 5 min per run and 100 temperatures, this would take 500 minutes, or 8 hours and 20 minutes.
I'm sorta on my old shit again.
"""
import numpy as np
import concurrent.futures
from metropolistwo import Metropolis2
import h5py
import multiprocessing

class Worker:
    def __init__(self,
                 temperature: float,
                 run: int,
                 ):
        self.T = temperature
        self.run = run
    
    def process(self):
        dim = (50, 50)
        m = Metropolis2(dim, self.T)
        # Contrary to the silly name I chose this is not a random state, but a fixed one
        # The fixed state was created randomly in the create-fixed-init.py script, hence the name
        # m.state = np.load("./IsingModel/Results/random-state.npy")
        m.MAX_ITER = 1e5
        m.quiet = True
        print(f"[INFO] Starting: T={self.T}\tRun={self.run}")
        s_init, s_final, en = m.run()

        return self.run, s_init, s_final, en, m.temperatures
    
# Create function that'll get the workders to work
def worker_task(params):
    worker = Worker(*params)
    return worker.process()

# Create function for thread-safe writing
def write_data(save_path, key, s_final, en, temps, lock):
    with lock:
        with h5py.File(save_path, "a") as f:
            group = f.create_group(f"{key}")
            dset_state = group.create_dataset(f"state-{key}", data=s_final,
                                            compression="gzip", compression_opts=9)
            dset_en = group.create_dataset(f"energy-{key}", data=en, compression="gzip",
                                        compression_opts=9)
            dset_t = group.create_dataset(f"temperature-{key}", data=temps, compression="gzip",
                                        compression_opts=9)
    
# Get Process Pool parameter list
runs = 100
param_list = np.genfromtxt("./IsingModel/Code/T_range.lst")
param_list = [[par, i] for par in param_list for i in range(runs)]

# Create manager and lock for thread-safe writing
manager = multiprocessing.Manager()
lock = manager.Lock()

# Run process pool and save on thread execution
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
    futures = [executor.submit(worker_task, params) for params in param_list]
    
    # Step 4: Collect the results
    for future in concurrent.futures.as_completed(futures):
        run, s_init, s_final, en, temps = future.result()
        arg1 = temps[0]
        arg2 = run
        save_path = "./IsingModel/Results/avgE-vs-T-v3.h5"
        print(f"Storing run {arg1},{arg2} to '{save_path}'..")
        write_data(save_path, f"{arg1}-{arg2}", s_final, en, temps, lock)
        print(f"Saved!")
