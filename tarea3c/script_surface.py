"""
    script_surface.py
    Script de visualización en forma de superficie
    Bryan Ortiz
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

V = np.load("solution.npy")

fig = plt.figure()
ax = fig.gca(projection='3d')

nh = len(V)
nv = len(V[0])

h = 10000/(nv-1)
# Make data.
X = np.arange(0, nh, 1) 
Y = np.arange(0, nv, 1) 
X, Y = np.meshgrid(X, Y)
Z = V.T

# Plot the surface.
surf = ax.plot_surface(X*h, Y*h, Z, cmap='RdBu_r', linewidth=0, antialiased=False)

# Customize the axis
plt.xlabel('Distance (x)')
plt.ylabel('Height (y)')
ax.set_zlabel('Potential (z)')
ax.set_title('Laplace Equation solution\nSurface visualization')
ax.ticklabel_format(style='sci', scilimits=(0,3))
ax.set_aspect('equal')
# Add a color bar which maps values to colors.
fig.colorbar(surf)

plt.show()