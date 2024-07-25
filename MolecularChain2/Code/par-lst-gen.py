import numpy as np

# sequence = np.logspace(np.log10(0.1), np.log10(100), num=100, endpoint=True)
sequence = np.linspace(0.8, 0.9999, num=100, endpoint=True)

with open('/home/pengu5055/Documents/FMF1mag/mod108/MolecularChain2/Code/aR_range.lst', 'w') as file:
    for number in sequence:
        file.write(f'{number}\n')