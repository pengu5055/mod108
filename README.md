# **Metropolis-Hastings Algorithm**
mod108 task for Model Analysis I course at UL FMF.

## Notes
You can enable mpl Interactive plots on Linux by exporting the following environment variable:
```bash
export MPLBACKEND=qtagg
```
or in `fish` which is what I use as my shell:
```fish
set -x MPLBACKEND qtagg
```
These two lines can be added to either `~/.bashrc` or `~/.config/fish/config.fish` to make the change permanent. I've also included two scripts for running multiple runs of a simulation for both `bash` and `fish`.

## Running the scripts for data gathering
Used like so:
```fish
  ./MolecularChain2/Code/run-T-aR-gridscan.fish $(which python) ./MolecularChain2/Code/T_range.lst ./MolecularChain2/Code/aR_range.lst 
```
where `$(which python)` is the path to the python interpreter in the `.venv`. The `T_range.lst` and `aR_range.lst` are the files containing the ranges of the parameters to scan over. The script will generate a file `./MolecularChain2/Results/par-gridscan-T-annealR.h5` with the results of the simulation.
