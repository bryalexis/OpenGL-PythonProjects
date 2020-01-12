"""
    script_img.py
    Script de visualización en forma de imagen
    Bryan Ortiz
"""
import numpy as np
import matplotlib.pyplot as mpl

V = np.load("solution.npy")
h = 20000/(len(V)-1)
X = np.arange(0, 20000+h, h)
Y = np.arange(0, 10000+h, h)


# Customize the axis.
fig, ax = mpl.subplots(1,1)
pcm = ax.pcolormesh(X, Y, V.T, cmap='RdBu_r')
ax.set_xlabel('Distance (x)')
ax.set_ylabel('Height (y)')
ax.set_title('Laplace equation solution.\n Neumann Condition at the crater of the volcano.')
ax.set_aspect('equal')
fig.colorbar(pcm)
mpl.show()