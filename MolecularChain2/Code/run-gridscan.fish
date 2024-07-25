#! /usr/bin/env fish

# Specify where the .venv python binary is contained
set py_spec $argv[1]
set T_range (cat $argv[2])
set aR_range (cat $argv[3])

for T in $T_range
    for aR in $aR_range
        echo "Running T = $T, aR = $aR"
        $py_spec ./MolecularChain2/Code/par-gridscan.py $T $aR
    end
end