import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(1)
ax = fig.add_subplot(111)

x = np.arange(-2*np.pi, 2*np.pi, 0.1)
ax.plot(x, np.sin(x), label='Sine')
ax.plot(x, np.cos(x), label='Cosine')
ax.plot(x, np.arctan(x), label='Inverse tan')

lgd = ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5,-0.1),
    ncol = 1
)

ax.grid('on')

fig.savefig(
    'samplefigure.pdf',
    bbox_extra_artists=(lgd,),
    bbox_inches='tight'
)