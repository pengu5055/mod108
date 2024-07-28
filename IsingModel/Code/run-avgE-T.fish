#! /usr/bin/env fish

# Specify where the .venv python binary is contained
set py_spec $argv[1]
set T_range (cat $argv[2])

for T in $T_range
    echo "Running T = $T"
    $py_spec ./IsingModel/Code/avgE-vs-T.py $T
end