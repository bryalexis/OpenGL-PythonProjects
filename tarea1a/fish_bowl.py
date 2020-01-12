# coding=utf-8
"""

    Bryan Ortiz, CC3501, 2019-1
    Tarea 1A - fish_bowl

"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import random as r
import transformations as tr
import sys


# We will use 32 bits data, an integer with 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4

"""
    ---------------< Container & Classes >---------------
"""

# A class that saves all the data from fishes
class Fish:
    def __init__(self, position, tipo, movement, scale, x, ubication):
        self.tipo = tipo                  # Tipo de pez (1 -> Mora, 2-> Nemo, 3-> Globo)
        self.position = position          # Posición donde se crea el pez
        self.movement = movement          # Tipo de movimiento entre los disponibles 
        self.scale = scale                # Factor de escalamiento uniforme del pez
        self.ubicationInTime = ubication  # Guarda la posición del pez en tiempo real
        self.factor = x                   # Constante que define parámetros del movimiento del pez
        
# Random position
def shufflePos():
    return r.randrange(-80,80,1)/160

# Random type of movement
def shuffleMov():
    return r.randrange(1,6,1)

# Random size from 0.5 to 1.0
def shuffleSize():
    return r.randrange(40,131,1)/100

# Random movement factor
def shuffleFactor():
    return r.randrange(1,10,1)

# Random type of fish
def shuffleFishType():
    return int(r.randrange(1,4))

# A class for the bubbles
class Bubble:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size

# A container class for the fishes
class FishBowl:
    
    def __init__(self):
        self.fishes = [ Fish( [ shufflePos(), shufflePos(), 0.0], 1, shuffleMov(), shuffleSize(), shuffleFactor(), [0,0,0]),
            Fish( [ shufflePos(), shufflePos(), 0.0], 2, shuffleMov(), shuffleSize(), shuffleFactor(), [0,0,0]),
            Fish( [ shufflePos(), shufflePos(), 0.0], 3, shuffleMov(), shuffleSize(), shuffleFactor(), [0,0,0]),
            Fish( [ shufflePos(), shufflePos(), 0.0], 1, shuffleMov(), shuffleSize(), shuffleFactor(), [0,0,0]),
            Fish( [ shufflePos(), shufflePos(), 0.0], 2, shuffleMov(), shuffleSize(), shuffleFactor(), [0,0,0])]
        
        self.bubbles = [  ]

        for i in range(100):
            self.bubbles += [ Bubble( shufflePos()*6, shufflePos()*6, r.randrange(10,100)/2000 ) ]

    def deleteFish(self, i):
        updatedFishes = []
        for j in range(len(self.fishes)):
            if j!=i:
                updatedFishes += [self.fishes[j]]
        self.fishes = updatedFishes

# A class to control the application
class Controller:
    def __init__(self):
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = [ 0.0, 0.0 ]
        self.screenWidth = 600
        self.screenHeight = 600


# We will use the global controller as communication with the callback function
controller = Controller()
FishBowl = FishBowl()

# On Key functions 
# Esc -> Exit
# Enter -> Adds a Fish
def on_key(window, key, scancode, action, mods):

    if action == glfw.PRESS:

        # Closes the window
        if key == glfw.KEY_ESCAPE:
            print("[EXIT]: Adiós.")
            sys.exit()

        # Adds a new fish
        if key == glfw.KEY_ENTER:
            
            # Adds a new fish in the FishBowl
            FishBowl.fishes += [ Fish( [ shufflePos(), shufflePos(), 0.0], shuffleFishType(), shuffleMov(), shuffleSize(), shuffleFactor(), [0,0,0])]
            
            # Prints the updated number of fishes
            print("[ADD]: Pez añadido, ahora hay "+str(len(FishBowl.fishes))+" peces.")

# Gets the position of the mouse
def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = [(2*x)/controller.screenHeight-1,(-y*2)/controller.screenWidth+1]

# Mouse functions
def mouse_button_callback(window, button, action, mods):

    global controller

    # Click to delete a fish
    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = True

# Scroll
def scroll_callback(window, x, y):

    print("Mouse scroll:", x, y)

# Container class to reference the shapes on GPU
class GPUShape:
    vao = 0
    vbo = 0
    ebo = 0
    size = 0

# Draws the shape
def drawShape(shaderProgram, shape, transform):

    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


"""
    ------------< Simple Figures >-------------
"""

# Creates a Square with the colors delivered at the vertices
# colors = [4][3] -> 4 colors with 3 components RGB
def createSquare(colors):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    #Colors
    c1 = colors[0]
    c2 = colors[1]
    c3 = colors[2]
    c4 = colors[3]
    
    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   Positions         Colors
        -0.5, -0.5, 0.0,  c1[0], c1[1], c1[2],
         0.5, -0.5, 0.0,  c2[0], c2[1], c2[2],
         0.5,  0.5, 0.0,  c3[0], c3[1], c3[2],
        -0.5,  0.5, 0.0,  c4[0], c4[1], c4[2],
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

# Creates a Triangle with the colors delivered at the vertices
# colors = [3][3] -> 3 colors with 3 components RGB
def createTriangle(colors):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    #Colors
    c1 = colors[0]
    c2 = colors[1]
    c3 = colors[2]

    # Defining the location and colors of each vertex  of the shape
    vertexData = np.array(
    #     positions       colors
        [-0.7, -0.7, 0.0, c1[0], c1[1], c1[2],
          0.7, -0.7, 0.0, c2[0], c2[1], c2[2],
          0.0,  0.7, 0.0, c3[0], c3[1], c3[2] ],
          dtype = np.float32) # It is important to use 32 bits data

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2], dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

# Creates a circle
# center = [3] -> 3 components RGB
# border = [3] -> 3 components RGB
def createCircle(center,border):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining the location and colors of each vertex  of the shape

    vertex = [0.0, 0.0, 0.0, center[0], center[1], center[2]] #Center
    indexing = []
    for j in range (91):
        i = (j/45)*np.pi
        vertex = vertex + [0.5*np.cos(i), 0.5*np.sin(i), 0, border[0], border[1], border[2] ]
        if(j>0):
            indexing = indexing + [0,j,j+1]
    vertexData = np.array(vertex, dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(indexing, dtype= np.uint32) 
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

"""
    -----------< More Complex Figures >----------
"""

# Cretes the Sand
def createSand():

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining the location and colors of each vertex  of the shape
    vertexData = [

                # Arena de Fondo (Back)
                -1.0, -1.00, 0.0,   90.0 / 255.0,  70.0 / 255.0, 10.0 / 255.0, #0
                -0.7, -1.00, 0.0,  120.0 / 255.0, 100.0 / 255.0, 20.0 / 255.0, #1
                -1.0, -0.61, 0.0,  200.0 / 255.0, 180.0 / 255.0, 40.0 / 255.0, #2
                -0.7, -0.58, 0.0,  220.0 / 255.0, 200.0 / 255.0, 60.0 / 255.0, #3
                -0.6, -0.58, 0.0,  230.0 / 255.0, 210.0 / 255.0, 60.0 / 255.0, #4
                -0.5, -1.00, 0.0,  100.0 / 255.0,  80.0 / 255.0, 20.0 / 255.0, #5
                -0.4, -0.60, 0.0,  200.0 / 255.0, 180.0 / 255.0, 40.0 / 255.0, #6
                -0.2, -0.60, 0.0,  210.0 / 255.0, 180.0 / 255.0, 20.0 / 255.0, #7
                 0.1, -1.00, 0.0,  100.0 / 255.0,  90.0 / 255.0, 20.0 / 255.0, #8
                 0.0, -0.59, 0.0,  220.0 / 255.0, 200.0 / 255.0, 60.0 / 255.0, #9
                 0.2, -0.60, 0.0,  210.0 / 255.0, 180.0 / 255.0, 20.0 / 255.0, #10
                 0.8, -0.70, 0.0,  180.0 / 255.0, 150.0 / 255.0, 10.0 / 255.0, #11
                 1.0, -1.00, 0.0,   90.0 / 255.0,  70.0 / 255.0, 10.0 / 255.0, #12
                 1.0, -0.73, 0.0,  170.0 / 255.0, 140.0 / 255.0, 20.0 / 255.0, #13

                # Arena de Fondo (Front)
                 1.0, -0.50, 0.0,  240.0 / 255.0, 220.0 / 255.0, 40.0 / 255.0, #14
                 0.9, -0.49, 0.0,  230.0 / 255.0, 225.0 / 255.0, 50.0 / 255.0, #15
                 0.8, -1.00, 0.0,  120.0 / 255.0,  90.0 / 255.0, 25.0 / 255.0, #16
                 0.8, -0.52, 0.0,  230.0 / 255.0, 210.0 / 255.0, 40.0 / 255.0, #17
                 0.6, -0.57, 0.0,  210.0 / 255.0, 180.0 / 255.0, 30.0 / 255.0, #18
                 0.6, -1.00, 0.0,  170.0 / 255.0, 140.0 / 255.0, 20.0 / 255.0, #19
                 0.4, -0.60, 0.0,  160.0 / 255.0, 150.0 / 255.0, 20.0 / 255.0, #20
                 0.3, -1.00, 0.0,  110.0 / 255.0,  90.0 / 255.0, 20.0 / 255.0, #21
                 0.3, -0.65, 0.0,  150.0 / 255.0, 140.0 / 255.0, 20.0 / 255.0, #22
                 0.2, -0.70, 0.0,  140.0 / 255.0, 130.0 / 255.0, 20.0 / 255.0, #23
                 0.1, -0.77, 0.0,  140.0 / 255.0, 120.0 / 255.0, 20.0 / 255.0, #24
                -0.2, -0.85, 0.0,  130.0 / 255.0, 120.0 / 255.0, 20.0 / 255.0, #25

                ]

    # 32 bits data
    vertexData = np.array(vertexData, dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [
            0, 1, 2,     2, 3, 1,       3, 4, 1,     1, 4, 5,     4, 5, 6,     
            6, 5, 7,     7, 5, 8,       7, 8, 9,     9, 10, 8,    10, 8, 11,
            8, 11, 12,   11, 12, 13,

            12, 14, 15,    15, 12, 16,     16, 15, 17,     17, 16, 18,     18, 16, 19,
            19, 18, 20,    20, 19, 21,     21, 20, 22,     22, 21, 23,     23, 21, 8,
            8, 23, 24,     8, 24, 25,      8, 25, 5         
         ], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO & EBO
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

# Creates the Water
def createWater():
    
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining the location and colors of each vertex  of the shape
    vertexData = [ -1, -1, 0,       10.0 / 255.0 ,  40.0 / 255.0 , 100.0 / 255.0,
                    1, -1, 0,       10.0 / 255.0 ,  40.0 / 255.0 , 100.0 / 255.0,
                    1,  1, 0,      160.0 / 255.0 , 200.0 / 255.0 , 255.0 / 255.0,
                   -1,  1, 0,      160.0 / 255.0 , 200.0 / 255.0 , 255.0 / 255.0 ]

    # 32 bits data
    vertexData = np.array(vertexData, dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array([
        0, 1, 2,    2, 3, 0
        ], dtype=np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO & EBO 
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

# Cretes diferent types of fishes
def createFishes(tipo):

    # Here the new shape will be stored
    gpuShape = GPUShape()
    vertexData = []
    indices = []

    # Type 1: Morita
    if (tipo==1):

        # Defining the location and colors of each vertex  of the shape
        vertexData = [

            # Cuerpecito
            0.00,  0.00, 0.0,  220.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #0

            -0.05,  0.05, 0.0,  220.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #1
            -0.08,  0.00, 0.0,  180.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #2
            -0.10,  0.05, 0.0,  220.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #3
            -0.14,  0.01, 0.0,  180.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #4
            -0.13,  0.00, 0.0,  180.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #5
            -0.14, -0.01, 0.0,  180.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #6
            -0.10, -0.05, 0.0,  220.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #7
            -0.05, -0.05, 0.0,  220.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #8

            # Colita
            -0.03,  0.00, 0.0,  220.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #9
            0.02,  0.03, 0.0,  255.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #10
            0.06,  0.03, 0.0,  255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, #11*
            0.02,  0.00, 0.0,  100.0 / 255.0, 100.0 / 200.0, 255.0 / 255.0, #12*
            0.02, -0.03, 0.0,  255.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #13
            0.06, -0.03, 0.0,  255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, #14

            # Choca esa aleta
            -0.05,  0.05, 0.0,  240.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #15
            -0.02,  0.08, 0.0,  255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, #16
            -0.10,  0.05, 0.0,  240.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #17
            -0.05, -0.05, 0.0,  240.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #18
            -0.02, -0.08, 0.0,  255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, #19
            -0.10, -0.05, 0.0,  240.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #20

            # Ojito
            -0.098, 0.020, 0.0,  255.0 / 255.0,  255.0 / 255.0, 255.0 / 255.0, #21
            -0.098, 0.032, 0.0,  255.0 / 255.0,  255.0 / 255.0, 255.0 / 255.0, #22
            -0.110, 0.020, 0.0,  255.0 / 255.0,  255.0 / 255.0, 255.0 / 255.0, #23
            -0.110, 0.032, 0.0,  255.0 / 255.0,  255.0 / 255.0, 255.0 / 255.0, #24
            -0.10,  0.020, 0.0,  0.0 / 255.0,  150.0 / 255.0, 50.0 / 255.0, #25
            -0.10,  0.030, 0.0,  0.0 / 255.0,  150.0 / 255.0, 50.0 / 255.0, #26
            -0.11,  0.020, 0.0,  0.0 / 255.0,  150.0 / 255.0, 50.0 / 255.0, #27
            -0.11,  0.030, 0.0,  0.0 / 255.0,  150.0 / 255.0, 50.0 / 255.0, #28

            # Otra aletita
            -0.08,  0.01, 0.0,  230.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #15
            -0.05,  0.00, 0.0,  255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, #16
            -0.08, -0.02, 0.0,  230.0 / 255.0,  10.0 / 255.0, 200.0 / 255.0, #17 
        ]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0,  1,  2,     1,  2,  3,     3,  2,  4,      4,  5,  2,     6,  5,  2, 
            6,  2,  7,     7,  2,  8,     8,  2,  0,      9, 10, 11,     9, 12, 11,     
            9, 13, 14,     9, 12, 14,    15, 16, 17,     18, 19, 20,    21, 22, 23,
           22, 23, 24,    25, 26, 27,    26, 27, 28,     29, 30, 31
        ]

    # Pez de tipo 2: Nemo
    elif (tipo==2):
        
        # Defining the location and colors of each vertex  of the shape
        vertexData = [

            #Cuerpo
            -0.10,  0.010, 0.0,    1.0, 0.0, 0.0, #0
            -0.10, -0.010, 0.0,    1.0, 0.0, 0.0, #1
            -0.05,  0.000, 0.0,    1.0, 0.0, 0.0, #2
            -0.05,  0.050, 0.0,    1.0, 0.0, 0.0, #3
            -0.05, -0.050, 0.0,    1.0, 0.0, 0.0, #4
             0.00,  0.000, 0.0,    1.0, 0.0, 0.0, #5
             0.00,  0.050, 0.0,    1.0, 0.0, 0.0, #6
             0.00, -0.050, 0.0,    1.0, 0.0, 0.0, #7
             0.10,  0.015, 0.0,    1.0, 0.0, 0.0, #8
             0.10, -0.015, 0.0,    1.0, 0.0, 0.0, #9

            # Cola
            0.180,  0.040, 0.0,   1.0, 0.0, 0.0, #10
            0.190,  0.000, 0.0,   1.0, 0.0, 0.0, #11
            0.185, -0.025, 0.0,   1.0, 0.0, 0.0, #12

            # Manchas
            0.125,  0.0225, 0.0,  1.0, 1.0, 1.0, #13
            0.125, -0.0175, 0.0,  1.0, 1.0, 1.0, #14
            
            -0.075,  0.0300, 0.0,  1.0, 0.0, 0.0, #15
            -0.060,  0.0425, 0.0,  1.0, 1.0, 1.0, #16
            -0.075, -0.0300, 0.0,  1.0, 0.0, 0.0, #17
            -0.060, -0.0425, 0.0,  1.0, 1.0, 1.0, #18
            -0.070,  0.0000, 0.0,  1.0, 0.0, 0.0, #19
            -0.055,  0.0000, 0.0,  1.0, 1.0, 1.0, #20

            -0.015,  0.050, 0.0,  1.0, 1.0, 1.0, #21
            -0.015,  0.035, 0.0,  1.0, 1.0, 1.0, #22
             0.000,  0.030, 0.0,  1.0, 1.0, 1.0, #23
            -0.025,  0.000, 0.0,  1.0, 1.0, 1.0, #24
            -0.010,  0.000, 0.0,  1.0, 1.0, 1.0, #25
            -0.015, -0.035, 0.0,  1.0, 1.0, 1.0, #26
             0.000, -0.030, 0.0,  1.0, 1.0, 1.0, #27
            -0.015, -0.050, 0.0,  1.0, 1.0, 1.0, #28

            0.020,  0.0425, 0.0,  1.0, 1.0, 1.0, #29
            0.035,  0.0375, 0.0,  1.0, 0.0, 0.0, #30
            0.020, -0.0425, 0.0,  1.0, 1.0, 1.0, #31
            0.035, -0.0375, 0.0,  1.0, 0.0, 0.0, #32

            # Aletas
             0.00,  0.065, 0.0,   1.0, 1.0, 1.0, #33
             0.00, -0.070, 0.0,   1.0, 1.0, 1.0, #34
            -0.03, -0.070, 0.0,   0.0, 0.0, 0.0, #35

            0.10,  0.03, 0.0,   1.0, 1.0, 1.0, #36
            0.10, -0.03, 0.0,   1.0, 1.0, 1.0, #37

            # Ojos
            -0.085, 0.010, 0.0,  1.0, 1.0, 1.0, #38
            -0.085, 0.017, 0.0,  1.0, 1.0, 1.0, #39
            -0.078, 0.010, 0.0,  1.0, 1.0, 1.0, #40
            -0.078, 0.017, 0.0,  1.0, 1.0, 1.0, #41

            -0.085, 0.010, 0.0,  0.0, 0.0, 1.0, #42
            -0.085, 0.015, 0.0,  0.0, 0.0, 1.0, #43
            -0.080, 0.010, 0.0,  0.0, 0.0, 1.0, #44
            -0.080, 0.015, 0.0,  0.0, 0.0, 1.0, #45
            
        ]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0,  1,  2,      0,  2,  3,      1,  2,  4,      3,  6,  2,      4,  2,  7,
            6,  2,  7,      7,  5,  9,      6,  5,  8,      8,  5,  9,      8,  9, 10,
            9, 10, 12,     10, 11, 12,      8, 13, 14,      9,  8, 14,     15, 16, 20,
           15, 19, 20,     17, 18, 19,     19, 18, 20,     21,  6, 23,     21, 22, 23,
           23, 24, 25,     24, 23, 22,     24, 25, 26,     25, 26, 27,     26, 27, 28,
           28, 27,  7,     29, 30, 31,     30, 31, 32,      3, 33,  6,      4, 35,  7,
            7, 35, 34,      6,  8, 36,      7,  9, 37,     38, 39, 40,     39, 40, 41,
           42, 43, 44,     43, 44, 45
        ]

    # Pez de tipo 3: Pez Globo
    else:
        
        # Defining the location and colors of each vertex  of the shape
        vertexData = [0,0,0, 0.1, 1.0, 0.1]
        vertexData += [
            # Cola
            0.03,  0.0, 0.0, 10/255.0, 10/255.0, 211/255.0, #2
            0.09,  0.0, 0.0, 10/255.0, 10/255.0, 211/255.0, #3
            0.12,  0.04, 0.0, 0.1, 1.0, 0.1, #4
            0.12, -0.04, 0.0, 0.1, 1.0, 0.1, #5
        ]
        indices = [ 1, 2, 3,    1, 2, 4]
        for i in range(182):
            theta = (i/90)*np.pi
            j=i+5
            vertexData += [0.08*np.sin(theta)+0.008*np.cos(theta*18.1),0.08*np.cos(theta)+0.008*np.sin(theta*18.1),0, 10/255.0, 0.7+np.abs(np.sin(theta/30))/2, 10/255.0]
            if i>0: indices += [0,j-1,j]            

        vertexData += [

            # Ojos
            -0.020, 0.020, 0.0,  1.0, 1.0, 1.0, #187
            -0.020, 0.034, 0.0,  1.0, 1.0, 1.0, #188
            -0.034, 0.020, 0.0,  1.0, 1.0, 1.0, #189
            -0.034, 0.034, 0.0,  1.0, 1.0, 1.0, #190

            -0.024, 0.020, 0.0,  0.0, 0.0, 1.0, #33
            -0.024, 0.030, 0.0,  0.0, 0.0, 1.0, #34
            -0.034, 0.020, 0.0,  0.0, 0.0, 1.0, #35
            -0.034, 0.030, 0.0,  0.0, 0.0, 1.0, #36

            # Aletas
            0.0, 0.02, 0.0, 10/255.0, 10/255.0, 211/255.0,
            0.0, -0.02, 0.0, 10/255.0, 10/255.0, 211/255.0,
            0.05, 0.0, 0.0, 110/255.0, 210/255.0, 111/255.0,
        ]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices += [ 187, 188, 189,     188, 189, 190,     191, 192, 193,     192, 193, 194,    195, 196, 197 ]



    # 32 bits data
    vertexData = np.array(vertexData, dtype = np.float32)
    indices = np.array(indices, dtype= np.uint32)
    gpuShape.size = len(indices)

    # VAO, VBO & EBO
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


"""
    ---------------< Movements >---------------
"""
# Returns a position in the limits
def posInLimits(x,y):
    if x > 0.95: x = 0.95
    if x < -0.95: x = -0.95
    if y > 0.95: y = 0.95 
    if y < -0.95: y = -0.95
    return [x,y]

# Define a movement transformation with the data delivered
def setTransform(n, theta, translation, scale, x):

    t = translation
    shearing = tr.shearing(0.1*np.sin(theta),0.1*np.cos(theta),0,0,0,0)
    scale = tr.uniformScale(scale)
    theta = theta/4

    if n==1:
        tx = 0.7*np.cos(theta/(2*x))
        ty = 0.4*np.cos(theta/x) + 0.3*np.cos(theta)
    elif n==2:
        tx = 0.4*np.sin(theta) + 0.7*np.cos(theta/2)
        ty = 0.2*np.sin(theta)*np.cos(theta/x) + 0.1*np.sin(theta)
    elif n==3:
        tx = 0.5*np.cos(theta)*np.sin(theta/(2*x))+0.4*np.cos(theta)
        ty = 0.2*np.cos(theta)*np.sin(theta/x)+0.3*np.cos(theta)
    elif n==4:
        tx = 0.4*np.cos(theta/x)*np.cos(theta)
        ty = 0.2*np.cos(theta/(x))
    elif n==5:
        tx = 0.4*np.cos(theta/x)*np.sin(theta/x)
        ty = 0.2*np.cos(theta/x)*np.sin(theta)*np.cos(theta)
    else: 
        return tr.identity()

    tx = t[0] + tx
    ty = t[1] + ty
    pos = posInLimits(tx,ty)     
    translation = tr.translate(pos[0], pos[1], 0)

    return tr.matmul([ shearing, scale, translation ])

# Returns True if the fish is close to the click
def isNearTo(fish, click):
    if (fish[0] < click[0]+0.1) and (fish[0] > click[0]-0.1) and (fish[1] < click[1]+0.1) and (fish[1] > click[1]-0.1):
        return True
    else:
        return False
    
# Fish exterminator :(
def updateFishes(i,fishes):
    updatedFishes = []
    for j in range(len(fishes)):
        if j!=i:
            updatedFishes += [fishes[j]]
    return updatedFishes
        


"""
    ---------------< MAIN >---------------
"""

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    # Screen Size
    width = controller.screenWidth
    height = controller.screenHeight

    window = glfw.create_window(width, height, "Fishbowl by Bryan Ortiz", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Connecting callback functions to handle mouse events:
    # - Cursor moving over the window
    # - Mouse buttons input
    # - Mouse scroll
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
    
    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    water = createWater()
    sand = createSand()

    # Setting some colors
    violet = [ 205/255.0, 100/255.0, 210/255.0]
    darkViolet = [ 130/255.0, 80/255.0, 180/255.0]
    lightBlue = [ 160/255.0, 190/255.0, 209/255.0]
    darkGreen = [ 0,0.8,0 ] 
    lightGreen = [0.3,1,0.3]
    lightGray = [0.8,0.8,0.8]
    gray = [0.4,0.4,0.4]

    # Some simple figures
    lightBlueCircle = createCircle( lightBlue, [1,1,1] )
    blackCircle = createCircle([0,0,0],[0,0,0])
    violetSquare = createSquare([ violet, violet, violet, violet ])
    darkVioletSquare = createSquare([ violet, violet, darkViolet, darkViolet ])
    greenSquare = createSquare([ darkGreen, lightGreen, darkGreen, lightGreen ])
    grayCircle = createCircle(lightGray,gray)
    
    # Creates the first 5 fishes
    fishes = []
    for fish in FishBowl.fishes:
        fishes += [createFishes(fish.tipo)]
    size = 5
    
    while not glfw.window_should_close(window):
        
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling the shapes
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Using the time as the theta parameter
        theta = glfw.get_time()
        
        # If a new fish is added
        if (len(FishBowl.fishes)>size):
            fishes += [createFishes(FishBowl.fishes[len(FishBowl.fishes)-1].tipo)]  
            size = len(FishBowl.fishes)  

        # If a fish is clicked :(
        if (controller.leftClickOn):

            # Shows where the click was
            print("[CLICK]: En " + str(controller.mousePos) )

            # Searchs the fish in that ubication
            # The list is traversed in the opposite direction to eliminate the fish that is most over
            for c in range(len(FishBowl.fishes),0,-1):
                i = c-1
                # Defines a fish
                fish = FishBowl.fishes[i]

                if isNearTo(fish.ubicationInTime, controller.mousePos):

                    # The fish is killed by the program </3
                    FishBowl.deleteFish(i)

                    # The number of fish decreases 
                    size -= 1

                    # Deletes the remaining data
                    fishes = updateFishes(i,fishes)
                    print("[DELETE]: Pez "+str(i+1)+" fue asesinado por tu click.")
                    break

            print("[INFO]: Ahora hay "+str(len(FishBowl.fishes))+" pececitos")
            controller.leftClickOn = False
        

        # DRAWING THE SCENES

        # Water
        drawShape(shaderProgram, water, tr.identity())

        # Bubbles
        for i in range(100):
            bubble = FishBowl.bubbles[i]
            drawShape(shaderProgram, lightBlueCircle, tr.matmul([
                tr.uniformScale( bubble.size ),
                tr.translate(bubble.x+0.2*np.sin(theta/4), bubble.y+0.003, 0.0) ]) )
            FishBowl.bubbles[i].y +=0.003
            if FishBowl.bubbles[i].y > 1: FishBowl.bubbles[i].y = -1

        # Little Castle
        drawShape(shaderProgram, violetSquare, tr.matmul([ tr.scale(0.04,0.1,0), tr.translate(-0.755,-0.38,0.0) ]) )
        drawShape(shaderProgram, violetSquare, tr.matmul([ tr.scale(0.04,0.1,0), tr.translate(-0.645,-0.38,0.0) ]) )
        drawShape(shaderProgram, violetSquare, tr.matmul([ tr.scale(0.03,0.05,0), tr.translate(-0.7,-0.38,0.0) ]) )
        drawShape(shaderProgram, violetSquare, tr.matmul([ tr.scale(0.15,0.45,0), tr.translate(-0.7,-0.63,0.0) ]) )
        drawShape(shaderProgram, blackCircle, tr.matmul([ tr.scale(0.05,0.25,0), tr.translate(-0.7,-0.63,0.0) ]) )
        drawShape(shaderProgram, darkVioletSquare, tr.matmul([ tr.scale(0.15,0.02,0), tr.translate(-0.7,-0.58,0.0) ]) )
        
        # Algae
        for j in range(14):
            for i in range(4):
                drawShape(shaderProgram, greenSquare, tr.matmul([tr.scale(0.02,0.05,0), tr.shearing(0.2*np.sin(20*theta), 0.1*np.cos(theta),0,0,0,0), tr.translate(0.5+j*0.04,-0.6+i*0.08+j*0.002,0) ]))
                drawShape(shaderProgram, greenSquare, tr.matmul([tr.scale(0.02,0.05,0), tr.shearing(-0.2*np.sin(20*theta), 0.1*np.cos(theta),0,0,0,0), tr.translate(0.5+j*0.04,-0.64+i*0.08+j*0.002,0) ]))
                drawShape(shaderProgram, greenSquare, tr.matmul([tr.scale(0.02,0.05,0), tr.shearing(0.2*np.sin(20*theta), 0.1*np.cos(theta),0,0,0,0), tr.translate(-0.8-j*0.04,-0.58+i*0.08+j*0.002,0) ]))
                drawShape(shaderProgram, greenSquare, tr.matmul([tr.scale(0.02,0.05,0), tr.shearing(-0.2*np.sin(20*theta), 0.1*np.cos(theta),0,0,0,0), tr.translate(-0.8-j*0.04,-0.62+i*0.08+j*0.002,0) ]))
        
        # Marine stones
        drawShape(shaderProgram, grayCircle, tr.matmul([tr.scale(0.1,0.12,0), tr.translate(0.47,-0.6,0)]))
        drawShape(shaderProgram, grayCircle, tr.matmul([tr.scale(0.07,0.08,0), tr.translate(0.40,-0.62,0)]))
        drawShape(shaderProgram, grayCircle, tr.matmul([tr.scale(0.15,0.1,0), tr.translate(-0.8,-0.6,0)]))
        drawShape(shaderProgram, grayCircle, tr.matmul([tr.scale(0.08,0.08,0), tr.translate(-0.9,-0.6,0)]))
        drawShape(shaderProgram, grayCircle, tr.matmul([tr.scale(0.1,0.15,0), tr.translate(-0.58,-0.6,0)]))

        # Sand
        drawShape(shaderProgram, sand, tr.identity())

        # Fishes
        for i in range(len(FishBowl.fishes)):

            # Defines the movement's transform
            fish = FishBowl.fishes[i]
            typeOfMovement = fish.movement
            fishPosition = fish.position
            scaleSize = fish.scale
            scalar = fish.factor
            transform = setTransform( typeOfMovement, theta, fishPosition, scaleSize, scalar)
        
            # Positions and the future of Mr. fish 
            # ( He/She will be a great fish someday and I will be very proud )
            pastPosition = FishBowl.fishes[i].ubicationInTime
            newPosition = [transform[3][0], transform[3][1], 0]
            changeOfDirection = (newPosition[0] > pastPosition[0])
            
            if changeOfDirection:
                reflex = tr.reflexX()
                transform = tr.matmul([reflex, transform])

            # Draws the fish
            drawShape(shaderProgram, fishes[i], transform)

            # Saves the actual position of the fish
            FishBowl.fishes[i].ubicationInTime = newPosition

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
    