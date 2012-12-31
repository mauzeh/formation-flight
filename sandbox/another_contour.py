import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

#x = np.arange(-3, 4, 1)
#y = np.arange(-3, 4, 1)
#
#X, Y = np.meshgrid(x, y)
#
#ellipses = X*X + Y*Y
#
#print 'X = %s' % X
#print 'Y = %s' % Y
#print "ellipses = \n%s" % ellipses

z = np.array([
    [18, 13, 10,  9, 10, 13, 18],
    [13,  8,  5,  4,  5,  5, 13],
    [10,  5,  2,  1,  2,  5, 10],
    [ 9,  4,  1,  0,  1,  4,  9],
    [10,  5,  2,  1,  2,  5, 10],
    [13,  8,  5,  4,  5,  8, 13],
    [18, 13, 10,  9, 10, 13, 18],
])

x = np.array([1, 2, 4, 8, 16, 32, 64])
y = np.array([1, 2, 3, 4, 5, 6, 7])
v = [1, 2, 4, 5, 8, 13, 18]

x, y = np.meshgrid(x, y)

cs = plt.contour(x, y, z, v)
plt.clabel(cs)
plt.show()

x, y = np.mgrid[-1:1:7j,-1:1:7j]

plt.figure()
plt.contour(x,y,z)
plt.colorbar()
plt.title("Sparsely sampled function.")
plt.show()

xnew, ynew = np.mgrid[-1:1:100j,-1:1:100j]
tck = interpolate.bisplrep(x,y,z,s=1)
znew = interpolate.bisplev(xnew[:,0],ynew[0,:],tck)

plt.figure()
plt.contour(xnew,ynew,znew)
plt.colorbar()
plt.title("Interpolated function.")
plt.show()

