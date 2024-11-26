import numpy as np
from enum import Enum


np_array = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])
print(f"np_array:\n{np_array}")
print(f"np_array.sum(): {np_array.sum()}")
np_array = np.flip(np_array)
print(f"reverse of np_array:\n{np_array}")


