import numpy as np
from sympy import Symbol

def symbols_list(shape, fmt):
    if len(shape) == 1:
        return np.array([Symbol(fmt.format(i)) for i in range(shape[0])])
    elif len(shape) == 2:
        arr = np.empty(shape, dtype=object)
        for i in range(shape[0]):
            for j in range(shape[1]):
                arr[i][j] = Symbol(fmt.format(i, j))
        return arr
    raise ValueError("Only 1D/2D supported")
