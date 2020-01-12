"""
    script_levelCurves.py
    Script de visualización en forma de curvas de nivel
    Bryan Ortiz
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.pyplot as mpl

V = np.load("solution.npy")

nh = len(V) - 2
nv = len(V[0]) - 2
h = 20000/nh

# Make data.
X = np.arange(0, nh+2, 1)
Y = np.arange(0, nv+2, 1)
X, Y = np.meshgrid(X, Y)
Z = V.T

# Customize the axis.
fig, ax = mpl.subplots(1,1)
pcm = mpl.contour(X*h, Y*h, Z, cmap='RdBu_r')
ax.set_xlabel('Distance (x)')
ax.set_ylabel('Height (y)')
ax.set_title('Laplace Equation solution\nLevel Curves visualization')
ax.set_xlim(left=-h,right=20000+h)
ax.set_ylim(bottom=0,top=10000+h)
ax.set_aspect('equal')
fig.colorbar(pcm)

mpl.show()