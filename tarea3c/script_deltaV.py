# coding=utf-8
"""
Bryan Ortiz, CC3501 
Tarea 3C - Tormenta en Erupción Volcánica
Cálculo de E
"""

import numpy as np
import scipy as sc
import matplotlib.pyplot as mpl
import scipy.sparse as sp
import scipy.sparse.linalg  as la
import sys
from volcanic_eruption import volcanic_Eruption


# Grid Spacing
h = 250
# Electric Field Value
E = 0
# Delta V
diff = 0
# Vectors with the values
Ef = []
D = []
Vc = []
Vs = []

# Iterating through many values of E
while diff < 3*10**6:
    
    E += 100
    Ef.append(E)
    V = volcanic_Eruption(h,E)
    #print("======================================")
    vcrater = V[int(10000/h)+1][int(2500/h)+2]
    Vc.append(vcrater)
    #print("V Crater: " + str(vcrater))
    vsky = V[int(10000/h)+2][int(7500/h)+2]
    Vs.append(vsky)
    #print("V Cielo: " + str(vsky))
    diff = vcrater - vsky
    D.append(diff)
    #print("(-) " + str(diff))

mpl.xlabel("Magnitud de E")
mpl.ylabel("Potencial")
mpl.grid()
mpl.title("Diferencia de Potencial\n (mayor a 3M en E="+str(E)+")")
mpl.plot(Ef,Vs,label='Cielo',color='blue')
mpl.plot(Ef,Vc,label='Crater',color='red')
mpl.plot(Ef,D,label='Diferencia',color='purple')
mpl.legend(loc='upper right')
mpl.ticklabel_format(style='sci', scilimits=(0,4))
mpl.show()