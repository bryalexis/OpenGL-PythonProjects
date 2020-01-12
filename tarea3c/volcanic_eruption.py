# coding=utf-8
"""
Bryan Ortiz, CC3501 
Tarea 3C - Tormenta en Erupción Volcánica
Main Program
"""

import numpy as np
import scipy as sc
import matplotlib.pyplot as mpl
import scipy.sparse as sp
import scipy.sparse.linalg  as la
import sys
from functions import *


def volcanic_Eruption(h,E):
    # Width and Height
    W = 20000
    H = 10000
    # Boundary Dirichlet Conditions:
    BORDER = 0

    # The borders are totally known (Dirichlet condition)
    # The crater of the volcano is unknown (Neumann condition)
    nh = int(W / h) - 1
    nv = int(H / h) - 1

    # Dimensions of the grid
    #print(nh, nv)

    # In this case, the domain is just a rectangle
    N = nh * nv

    # We define a function to convert the indices from i,j to k and viceversa
    # i,j indexes the discrete domain in 2D.
    # k parametrize those i,j, this way we can tidy the unknowns
    # in a column vector and use the standard algebra

    def getK(i,j):
        return j * nh + i

    def getIJ(k):
        i = k % nh
        j = k // nh
        return (i, j)


    # In this matrix we will write all the coefficients of the unknowns
    # A lil_matrix is more efficent to construct a new sparse matrix from scratch
    A = sp.lil_matrix((N,N))

    # In this vector we will write all the right side of the equations
    b = np.zeros((N,))

    # Note: To write an equation is equivalent to write a row in the matrix system

    # We iterate over each point inside the domain
    # Each point has an equation associated
    # The equation is different depending on the point location inside the domain
    for i in range(0, nh):
        for j in range(0, nv):

            # We will write the equation associated with row k
            k = getK(i,j)

            # We obtain indices of the other coefficients
            k_up = getK(i, j+1)
            k_down = getK(i, j-1)
            k_left = getK(i-1, j)
            k_right = getK(i+1, j)

            # Depending on the location of the point, the equation is different
            
            # Inside the rectangle
            if (1 <= i and i <= nh - 2) and (1 <= j and j <= nv - 2):
                
                # We get the position
                x = i*h
                y = j*h

                x_R = (i+1)*h # 1 right position
                x_L = (i-1)*h # 1 left position
                y_B = (j-1)*h # 1 bottom position

                # [Volcano border conditions]

                # Right-Dirichlet
                # if it's the slope on the left there is a border condition on the right
                if esCB_CuestaIzq(x_R,x,y):
                    if dentroDelVolcan(x,y_B):
                        A[k, k_up] = 1
                        A[k, k_left] = 1
                        A[k, k] = -4
                        b[k] = -BORDER
                    else:
                        A[k, k_down] = 1
                        A[k, k_up] = 1
                        A[k, k_left] = 1
                        A[k, k] = -4
                        b[k] = -BORDER

                # Left-Dirichlet
                # if it's the slope on the right there is a border condition on the left
                elif esCB_CuestaDer(x_L,x,y):
                    if dentroDelVolcan(x,y_B):
                        A[k, k_up] = 1
                        A[k, k_right] = 1
                        A[k, k] = -4
                        b[k] = -BORDER
                    else:     
                        A[k, k_up] = 1
                        A[k, k_down] = 1
                        A[k, k_right] = 1
                        A[k, k] = -4
                        b[k] = -BORDER
                
                # Neumann Crater
                elif esCB_Crater(y_B,x,y):
                    A[k, k_up] = 2
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k] = -4
                    b[k] = -2 * h * E

                # Outside the volcano
                elif fueraDelVolcan(x,y):
                    A[k, k_up] = 1
                    A[k, k_down] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k] = -4
                    b[k] = 0

                # Inside the volcano
                # The value of the voltage at these points is zero (out of domain)
                else:
                    A[k, k] = 1
                    b[k] = 0

            # [ DIRICHLET CONDITIONS ]

            # Left
            elif i == 0 and (1 <= j and j <= nv - 2):
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_right] = 1
                A[k, k] = -4
                b[k] = -BORDER
            
            # Right
            elif i == nh - 1 and (1 <= j and j <= nv - 2):
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k] = -4
                b[k] = -BORDER

            # Top
            elif 1 <= i and (i <= nh - 2 and j == nv - 1):
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_right] = 1
                A[k, k] = -4
                b[k] = -BORDER
            
            # Bottom
            elif 1 <= i and i <= nh - 2 and j == 0:
                # Outside the volcano   
                if fueraDelVolcan(i*h,j*h):
                    A[k, k_up] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k] = -4
                    b[k] = -BORDER
                # Else, the value of that point is zero (out of domain).
                else:
                    A[k, k] = 1
                    b[k] = -BORDER

            # corner lower left
            elif (i, j) == (0, 0):
                A[k, k] = 1
                b[k] = BORDER

            # corner lower right
            elif (i, j) == (nh - 1, 0):
                A[k, k] = 1
                b[k] = BORDER

            # corner upper left
            elif (i, j) == (0, nv - 1):
                A[k, k] = 1
                b[k] = BORDER

            # corner upper right
            elif (i, j) == (nh - 1, nv - 1):
                A[k, k] = 1
                b[k] = BORDER

            else:
                print("Point (" + str(i) + ", " + str(j) + ") missed!")
                print("Associated point index is " + str(k))
                raise Exception()


    # CSC sparse matrix format is more suitable/efficient in matrix operations
    M = A.tocsc()
    # Solving our system
    x = la.spsolve(M, b)

    # Now we return our solution to the 2d discrete domain
    # In this matrix we will store the solution in the 2d domain
    V = np.zeros((nh,nv))

    for k in range(0, N):
        i,j = getIJ(k)
        V[i,j] = x[k]

    # Adding the borders, as they have known values
    Vb = np.zeros((nh + 2, nv + 2))
    # The inside
    Vb[1:nh+1, 1:nv+1] = V[:,:]
    # Borders
    Vb[0:nh + 2, nv + 1] = BORDER   # Top
    Vb[0:nh + 2, 0] = BORDER        # Bottom
    Vb[0, 1:nv + 1] = BORDER        # Left
    Vb[nh+1, 1:nv + 1] = BORDER     # Right
    
    return Vb

if __name__ == "__main__":
    if len(sys.argv)< 4:
        print("Arguments missing")
        raise Exception()

    # Grid spacing
    h = float(sys.argv[1])
    print("Grid spacing: "+str(h))

    # Value of the electric field (normal = J)
    E = float(sys.argv[2])
    print("Electric field value: "+str(E))

    # Output filename
    filename = sys.argv[3]
    print("Output data filename: "+filename)
    V = volcanic_Eruption(h,E)
    # Saving Data
    np.save(filename,V)