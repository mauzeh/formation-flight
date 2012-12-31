import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

x = np.array([
    -30, -20, -10,
    -30, -20, -10,
    -30, -20, -10,
])

y = np.array([
    60, 60, 60,
    50, 50, 50,
    40, 40, 40,
])

z = np.array([
    0.9494, 0.9363, 0.9232, 
    0.9438, 0.9400, 0.8726, 
    0.9382, 0.9307, 0.8970,
])

x = x.reshape(3, 3)
y = y.reshape(3, 3)
z = z.reshape(3, 3)

plt.figure()
plt.contour(x, y, z)
plt.colorbar()
plt.title("Sparsely sampled function.")
plt.show()