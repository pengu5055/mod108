#! /usr/bin/env fish

# Run fixed-init.py multiple times to generate a pool of data
set py_spec $argv[1]
set py3 (command -v python3 > /dev/null; and echo "1"; or echo "0")
set py (command -v python > /dev/null; and echo "1"; or echo "0")

echo (which python3)

if test -n "$py_spec"
    for ITER in (seq 0 100)
        $py_spec ./MolecularChain2/Code/fixed-init.py $ITER
    end

else if test $py3 -eq 1
    for ITER in (seq 0 100)
        python3 ./MolecularChain2/Code/fixed-init.py $ITER
    end

else if test $py -eq 1
    for ITER in (seq 0 100)
        python ./MolecularChain2/Code/fixed-init.py $ITER
    end

else
    echo "No version of python can be found.."
    exit 1
end
