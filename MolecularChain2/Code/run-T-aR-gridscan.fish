#! /usr/bin/env fish

# Specify where the .venv python binary is contained
set py_spec $argv[1]
set T_range $argv[2]
set aR_range $argv[3]

for T in $T_range
    for aR in $aR_range
        $py_spec ./MolecularChain2/Code/fixed-init.py $T $aR
    end
end