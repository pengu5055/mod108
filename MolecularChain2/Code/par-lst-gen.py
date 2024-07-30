import numpy as np

sequence = np.logspace(np.log10(1e-8), np.log10(3), num=100, endpoint=True)
# sequence = np.linspace(1e-8, 3, num=100, endpoint=True)
# sequence = np.arange(1, 11, 1)

with open('/home/pengu5055/Documents/FMF1mag/mod108/IsingModel/Code/H_range.lst', 'w') as file:
    for number in sequence:
        file.write(f'{number}\n')