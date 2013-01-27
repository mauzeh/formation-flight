import matplotlib.pyplot as plt
import numpy as np


t = np.linspace(0,1,1024)
f = np.sin(10*t)*1e3
plt.plot(t,f)

ax = plt.gca()
ax.ticklabel_format(style='sci', axis='y')
ax.yaxis.major.formatter.set_powerlimits((0,0))

plt.show()