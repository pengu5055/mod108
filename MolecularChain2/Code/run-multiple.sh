#! /bin/bash

# Run fixed-init.py multiple times to generate a pool of data
py_spec=$1
py3=$(command -v python3 >/dev/null 2>&1)
py=$(command -v python >/dev/null 2>&1)

echo $(which python3)

if $py_spec; then
    for ITER in 0 .. 100
    do
        $py_spec ./MolecularChain2/Code/fixed-init.py $ITER
    done

elif $py3; then
    for ITER in 0 .. 100
    do
        python3 ./MolecularChain2/Code/fixed-init.py $ITER
    done

elif $py; then 
    for ITER in 0 .. 100
    do
        python ./MolecularChain2/Code/fixed-init.py $ITER
    done
else
    echo "No version of python can be found.."
    exit 1;
fi
