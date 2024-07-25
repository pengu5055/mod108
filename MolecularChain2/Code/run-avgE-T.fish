#! /usr/bin/env fish

# Specify where the .venv python binary is contained
set py_spec $argv[1]
set T_range (cat $argv[2])

for T in $T_range
    for run in (seq 1 100)
        echo "Running T = $T, Run = $run"
        $py_spec ./MolecularChain2/Code/avgE-vs-T.py $T $run
    end
end