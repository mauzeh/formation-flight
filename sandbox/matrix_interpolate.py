import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

x,y = np.mgrid[-1:1:20j,-1:1:20j]
z = (x+y)*np.exp(-6.0*(x*x+y*y))

plt.figure()
plt.pcolor(x,y,z)
plt.colorbar()
plt.title("Sparsely sampled function.")
plt.show()

xnew,ynew = np.mgrid[-1:1:100j,-1:1:100j]
tck = interpolate.bisplrep(x,y,z,s=0)
znew = interpolate.bisplev(xnew[:,0],ynew[0,:],tck)
plt.figure()
plt.pcolor(xnew,ynew,znew)
plt.colorbar()
plt.title("Interpolated function.")
plt.show()