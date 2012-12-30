import matplotlib.pyplot as plt
import numpy as np

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

ellipses = np.array([
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

cs = plt.contour(x, y, ellipses, [1, 2, 4, 5, 8, 13, 18])
plt.clabel(cs)

plt.show()