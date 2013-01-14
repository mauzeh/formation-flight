import numpy as np
import matplotlib.pyplot as plt
import math

count_hubs = 3

results_1 = np.array([5, 6, 5, 6, 7, 5, 4, 5, 5, 5])
results_2 = np.array([5, 5, 4, 4, 5, 6, 5, 4, 4, 5])
results_3 = np.array([4, 5, 4, 4, 3, 4, 4, 3, 5, 4])

data = np.array([results_1, results_2, results_3])

for array in data:
    print array
    
means = np.array([
    np.mean(data[0,:]),
    np.mean(data[1,:]),
    np.mean(data[2,:]),
])

errors = np.array([
    np.std(data[0,:]),
    np.std(data[1,:]),
    np.std(data[2,:]),
])

print means, errors

plt.grid(True)

(mean_line, caps, _) = plt.errorbar(
    np.arange(1, len(means)+1),
    means, yerr = errors, elinewidth = 2
)

mean_line.set_color('#000000')

for cap in caps:
    cap.set_markeredgewidth(2)

plt.xlim(0.5, 7.5)
plt.ylim(0, 10)
plt.show()