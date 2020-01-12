
# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
vertices and indices for simple shapes
Modified by Bryan Ortiz:
+ Cylinder
+ Sphere
+ Texture Sphere
+ Texture Cone
"""
import numpy as np
from ex_aux_4 import *
import ex_curves

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def createAxis(length=1.0):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
        -length,  0.0,  0.0, 0.0, 0.0, 0.0,
         length,  0.0,  0.0, 1.0, 0.0, 0.0,

         0.0, -length,  0.0, 0.0, 0.0, 0.0,
         0.0,  length,  0.0, 0.0, 1.0, 0.0,

         0.0,  0.0, -length, 0.0, 0.0, 0.0,
         0.0,  0.0,  length, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1,
         2, 3,
         4, 5]

    return Shape(vertices, indices)


def createSphere():

    # Defining the location and colors of each vertex  of the shape
    vertices = []
    indices = []
    n = 90
    dtheta = (np.pi/n)
    dphi = (2*np.pi/n)
    for i in range(n):
        theta = i*dtheta
        for j in range(n):
            phi = j*dphi
            
            #Vertices
            vertices += [ 
                # Vertex 1
                np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta),
                # Color 1
                0, (1+np.sin(theta))/2, (1+np.cos(phi))/2,
                
                # Vertex 2
                np.cos(phi+dphi)*np.sin(theta), np.sin(phi+dphi)*np.sin(theta), np.cos(theta),
                # Color 2
                0, (1+np.sin(theta))/2, (1+np.cos(phi+dphi))/2,

                # Vertex 3
                np.cos(phi+dphi)*np.sin(theta+dtheta), np.sin(phi+dphi)*np.sin(theta+dtheta), np.cos(theta+dtheta),
                # Color 3
                0, (1+np.sin(theta+dtheta))/2, (1+np.cos(phi+dphi))/2,

                # Vertex 4
                np.cos(phi)*np.sin(theta+dtheta), np.sin(phi)*np.sin(theta+dtheta), np.cos(theta+dtheta),
                # Color 4
                0, (1+np.sin(theta+dtheta))/2, (1+np.cos(phi))/2
                ]
            
            k = 4*(n*i+j)
            indices += [k, k+1, k+2,  k+2, k+3, k] 

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    return Shape(vertices, indices)


def createRainbowTriangle():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
         0.0,  0.5, 0.0,  0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowQuad():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
         0.5,  0.5, 0.0,  0.0, 0.0, 1.0,
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuad(image_filename, nx=1, ny=1):

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, -0.5, 0.0,  0, 0,
         0.5, -0.5, 0.0, nx, 0,
         0.5,  0.5, 0.0, nx, ny,
        -0.5,  0.5, 0.0,  0, ny]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    textureFileName = image_filename

    return Shape(vertices, indices, textureFileName)


def createTextureHex(image_filename, nx=1, ny=1):

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [0,0,0, 0.5,0.5 ]
    dphi = np.pi/3
    for i in range(6):
        vertices += [np.sin(i*dphi), np.cos(i*dphi), 0,   0.5+np.sin(i*dphi)/2, 0.5+np.cos(i*dphi)/2]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,   0, 2, 3,      0,3,4,       0,4,5,     0,5,6,      0,6,1]

    textureFileName = image_filename

    return Shape(vertices, indices, textureFileName)

def createRainbowCube():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,
         0.5, -0.5,  0.5,  0.0, 1.0, 0.0,
         0.5,  0.5,  0.5,  0.0, 0.0, 1.0,
        -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,
 
        -0.5, -0.5, -0.5,  1.0, 1.0, 0.0,
         0.5, -0.5, -0.5,  0.0, 1.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 0.0, 1.0,
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2, 2, 3, 0,
         4, 5, 6, 6, 7, 4,
         4, 5, 1, 1, 0, 4,
         6, 7, 3, 3, 2, 6,
         5, 6, 2, 2, 1, 5,
         7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorCube(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
        -0.5, -0.5,  0.5, r, g, b,
         0.5, -0.5,  0.5, r, g, b,
         0.5,  0.5,  0.5, r, g, b,
        -0.5,  0.5,  0.5, r, g, b,

        -0.5, -0.5, -0.5, r, g, b,
         0.5, -0.5, -0.5, r, g, b,
         0.5,  0.5, -0.5, r, g, b,
        -0.5,  0.5, -0.5, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2, 2, 3, 0,
         4, 5, 6, 6, 7, 4,
         4, 5, 1, 1, 0, 4,
         6, 7, 3, 3, 2, 6,
         5, 6, 2, 2, 1, 5,
         7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorCylinder(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [ 0.0, 0.5, 0.0, r, g, b,        0.0, -0.5, 0.0, r, g, b ]
    indices = []
    n = 180
    for i in range(n):
        theta = (2*np.pi/n)*i
        theta_next = (2*np.pi/n)*(i+1)
        vertices += [0.5*np.cos(theta), 0.5, 0.5*np.sin(theta), r, g, b] 
        vertices += [0.5*np.cos(theta), -0.5, 0.5*np.sin(theta), r, g, b]
        vertices += [0.5*np.cos(theta_next), 0.5, 0.5*np.sin(theta_next), r, g, b] 
        vertices += [0.5*np.cos(theta_next), -0.5, 0.5*np.sin(theta_next), r, g, b]
        indices += [ 0, 4*i+2, 4*i+4,   1, 4*i+3, 4*i+5,    4*i+2,4*i+3,4*i+4,  4*i+4, 4*i+5, 4*i+3 ]

    return Shape(vertices, indices)

def createColorTriangularPrism(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
         0.5, -0.5, -0.5, r, g, b,
         0.5,  0.5, -0.5, r, g, b,
        -0.5,  0.5,  0.5, r, g, b,
        -0.5, -0.5,  0.5, r, g, b,

        -0.5,  0.5, -0.5, r, g, b,
        -0.5, -0.5, -0.5, r, g, b,]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2, 2, 3, 0,
         1, 4, 2,
         1, 4, 5, 4, 5, 0,
         0, 5, 3,
         4, 2, 3, 2, 3, 5]

    return Shape(vertices, indices)


def createTextureCube(image_filename):

    # Defining locations and texture coordinates for each vertex of the shape  
    vertices = [
    #   positions         texture coordinates
    # Z+
        -0.5, -0.5,  0.5, 0, 0,
         0.5, -0.5,  0.5, 1, 0,
         0.5,  0.5,  0.5, 1, 1,
        -0.5,  0.5,  0.5, 0, 1,

    # Z-
        -0.5, -0.5, -0.5, 0, 0,
         0.5, -0.5, -0.5, 1, 0,
         0.5,  0.5, -0.5, 1, 1,
        -0.5,  0.5, -0.5, 0, 1,
        
    # X+
         0.5, -0.5, -0.5, 0, 0,
         0.5,  0.5, -0.5, 1, 0,
         0.5,  0.5,  0.5, 1, 1,
         0.5, -0.5,  0.5, 0, 1
,
 
    # X-
        -0.5, -0.5, -0.5, 0, 0,
        -0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5,  0.5, 1, 1,
        -0.5, -0.5,  0.5, 0, 1,

    # Y+
        -0.5,  0.5, -0.5, 0, 0,
         0.5,  0.5, -0.5, 1, 0,
         0.5,  0.5,  0.5, 1, 1,
        -0.5,  0.5,  0.5, 0, 1,

    # Y-
        -0.5, -0.5, -0.5, 0, 0,
         0.5, -0.5, -0.5, 1, 0,
         0.5, -0.5,  0.5, 1, 1,
        -0.5, -0.5,  0.5, 0, 1
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices, image_filename)

def createTextureSphere(image_filename):

    # Defining the location and colors of each vertex  of the shape
    vertices = []
    indices = []
    n = 40
    dtheta = (np.pi/n)
    dphi = (2*np.pi/n)
    for i in range(n):
        theta = i*dtheta
        for j in range(n):
            phi = j*dphi
            dt = 1/(n)
            #Vertices
            vertices += [ 
                # Vertex 1
                np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta),
                # Texture 1
                i*dt, 2*j*dt,
                
                # Vertex 2
                np.cos(phi+dphi)*np.sin(theta), np.sin(phi+dphi)*np.sin(theta), np.cos(theta),
                # Texture 2
                i*dt, 2*(j+1)*dt,

                # Vertex 3
                np.cos(phi+dphi)*np.sin(theta+dtheta), np.sin(phi+dphi)*np.sin(theta+dtheta), np.cos(theta+dtheta),
                # Texture 3
                (i+1)*dt, 2*(j+1)*dt,

                # Vertex 4
                np.cos(phi)*np.sin(theta+dtheta), np.sin(phi)*np.sin(theta+dtheta), np.cos(theta+dtheta),
                # Texture 4
                (i+1)*dt, 2*j*dt
                ]
            
            k = 4*(n*i+j)
            indices += [k, k+1, k+2,  k+2, k+3, k] 

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    return Shape(vertices, indices, image_filename)

def createTextureCone(image_filename):

    # Defining the location and colors of each vertex  of the shape
    vertices = [0, 0, 0,  0.5, 0.5]
    indices = []
    n = 40
    dtheta = (2*np.pi/n)
    for i in range(n):
        theta = i*dtheta
        #Vertices
        vertices += [ np.cos(theta), np.sin(theta), 1,   0.5+np.cos(theta)/2, 0.5+np.sin(theta)/2]
        vertices += [ np.cos(theta+dtheta), np.sin(theta+dtheta), 1,   0.5+np.cos(theta+dtheta)/2, 0.5+np.sin(theta+dtheta)/2]
        indices += [ 0, 2*i+1, 2*i+2 ] 

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    return Shape(vertices, indices, image_filename)

def createInsideSphere(image_filename):

    # Curve A
    C1 = np.array([[0, 1]]).T
    C2 = np.array([[0.1, 0.7]]).T
    C3 = np.array([[0.45, 0.5]]).T
    C4 = np.array([[0.7, 0.2]]).T
    C5 = np.array([[1, 0]]).T
    c1 = fix_data(catmull_rom(C1, C2, C3, C4, C5))
    curveA =[]
    for i in range(len(c1)):
        if i%4==0:
            a = (1+round(c1[i][0].item(),4))/2
            curveA += [a]
    
    # Curve B
    C1 = np.array([[1, 0]]).T
    C2 = np.array([[-0.2, 0.7]]).T
    C3 = np.array([[-0.7, 0.4]]).T
    C4 = np.array([[-0.9, 0.2]]).T
    C5 = np.array([[-1, 0]]).T
    c1 = fix_data(catmull_rom(C1, C2, C3, C4, C5))
    curveB =[]
    for i in range(len(c1)):
        if i%4==0:
            a = (1+round(c1[i][0].item(),4))/2
            b = (1+round(c1[i][1].item(),4))/2
            curveB += [a]
    curve = curveA+curveB
    n = int(len(curve))
    
    # Vertex and Index
    vertices = []
    indices = []
    # Set dTheta and dPhi
    dtheta = (np.pi/n)
    dphi = (2*np.pi/n)

    for i in range(n):
        theta = i*dtheta
        z = np.cos(theta)
        vertices += [ 0, 0, z,  0.5, 0.5]
        center = i*(2*n+1)
        for j in range(n):
            phi = j*dphi
            p =i
            # if i%2==0: p=i
            # else: p= i-1
            #Vertices
            vertices += [ 
                # Vertex 1
                np.cos(phi)*curve[p], np.sin(phi)*curve[p], z,
                # Texture 1
                (1+np.cos(phi))/2,(1+np.sin(phi))/2,
                
                # Vertex 2
                np.cos(phi+dphi)*curve[p], np.sin(phi+dphi)*curve[p], z,
                # Texture 2
                (1+np.cos(phi+dphi))/2, (1+np.sin(phi+dphi))/2
            ]
            indices += [center, center+2*j+1, center+2*j+2]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    return Shape(vertices, indices, image_filename)

def createRainbowNormalsCube():

    sq3 = 0.57735027

    # Defining the location and colors of each vertex  of the shape
    vertices = [
            -0.5, -0.5,  0.5, 1.0, 0.0, 0.0, -sq3, -sq3, sq3,
             0.5, -0.5,  0.5, 0.0, 1.0, 0.0,  sq3, -sq3,  sq3,
             0.5,  0.5,  0.5, 0.0, 0.0, 1.0,  sq3,  sq3,  sq3,
            -0.5,  0.5,  0.5, 1.0, 1.0, 1.0, -sq3,  sq3,  sq3,

            -0.5, -0.5, -0.5, 1.0, 1.0, 0.0, -sq3, -sq3, -sq3,
             0.5, -0.5, -0.5, 0.0, 1.0, 1.0,  sq3, -sq3, -sq3,
             0.5,  0.5, -0.5, 1.0, 0.0, 1.0,  sq3,  sq3, -sq3,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0, -sq3,  sq3, -sq3
            ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)

def createColorNormalTriangularPrism(r, g, b):

    r2 = 1 / np.sqrt(2)
    r10 = 10 / np.sqrt(10)
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors    normals
    # XZ+
         0.5, -0.5, -0.5, r, g, b, r2, 0, r2, # 0
         0.5,  0.5, -0.5, r, g, b, r2, 0, r2, # 1
        -0.5,  0.5,  0.5, r, g, b, r2, 0, r2, # 2
        -0.5, -0.5,  0.5, r, g, b, r2, 0, r2, # 3

    # Y+
        0.5, 0.5, -0.5, r, g, b, 0, 1, 0, # 4
        -0.5, 0.5, -0.5, r, g, b, 0, 1, 0,# 5
        -0.5, 0.5, 0.5, r, g, b, 0, 1, 0,# 6

    # Y-
        0.5, -0.5, -0.5, r, g, b, 0, -1, 0, # 7
        -0.5, -0.5, -0.5, r, g, b, 0, -1, 0, # 8
        -0.5, -0.5, 0.5, r, g, b, 0, -1, 0, # 9

    # X-
        -0.5, 0.5, -0.5, r, g, b, -1, 0, 0, # 10
        -0.5, 0.5, 0.5, r, g, b, -1, 0, 0, # 11
        -0.5, -0.5, 0.5, r, g, b, -1, 0, 0, # 12
        -0.5, -0.5, -0.5, r, g, b, -1, 0, 0, # 13

    # Z-
        0.5, 0.5, -0.5, r, g, b, 0, 0, -1, # 14
        -0.5, 0.5, -0.5, r, g, b, 0, 0, -1, # 15
        -0.5, -0.5, -0.5, r, g, b, 0, 0, -1, # 16
        0.5, -0.5, -0.5, r, g, b, 0, 0, -1, # 17
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2, 2, 3, 0,
         4, 5, 6,
         7, 8, 9,
         10, 11, 12, 12, 13, 10,
         14, 15, 16, 16, 17, 14]

    return Shape(vertices, indices)

def createColorNormalsCube(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions         colors   normals
    # Z+
        -0.5, -0.5,  0.5, r, g, b, 0,0,1,
         0.5, -0.5,  0.5, r, g, b, 0,0,1,
         0.5,  0.5,  0.5, r, g, b, 0,0,1,
        -0.5,  0.5,  0.5, r, g, b, 0,0,1,

    # Z-
        -0.5, -0.5, -0.5, r, g, b, 0,0,-1,
         0.5, -0.5, -0.5, r, g, b, 0,0,-1,
         0.5,  0.5, -0.5, r, g, b, 0,0,-1,
        -0.5,  0.5, -0.5, r, g, b, 0,0,-1,
        
    # X+
        0.5, -0.5, -0.5, r, g, b, 1,0,0,
        0.5,  0.5, -0.5, r, g, b, 1,0,0,
        0.5,  0.5,  0.5, r, g, b, 1,0,0,
        0.5, -0.5,  0.5, r, g, b, 1,0,0,
 
    # X-
        -0.5, -0.5, -0.5, r, g, b, -1,0,0,
        -0.5,  0.5, -0.5, r, g, b, -1,0,0,
        -0.5,  0.5,  0.5, r, g, b, -1,0,0,
        -0.5, -0.5,  0.5, r, g, b, -1,0,0,

    # Y+
        -0.5, 0.5, -0.5, r, g, b, 0,1,0,
         0.5, 0.5, -0.5, r, g, b, 0,1,0,
         0.5, 0.5,  0.5, r, g, b, 0,1,0,
        -0.5, 0.5,  0.5, r, g, b, 0,1,0,

    # Y-
        -0.5, -0.5, -0.5, r, g, b, 0,-1,0,
         0.5, -0.5, -0.5, r, g, b, 0,-1,0,
         0.5, -0.5,  0.5, r, g, b, 0,-1,0,
        -0.5, -0.5,  0.5, r, g, b, 0,-1,0
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices)


def createTextureNormalsCube(image_filename):

    # Defining locations,texture coordinates and normals for each vertex of the shape  
    vertices = [
    #   positions            tex coords   normals
    # Z+
        -0.5, -0.5,  0.5,    0, 0,        0,0,1,
         0.5, -0.5,  0.5,    1, 0,        0,0,1,
         0.5,  0.5,  0.5,    1, 1,        0,0,1,
        -0.5,  0.5,  0.5,    0, 1,        0,0,1,   
    # Z-          
        -0.5, -0.5, -0.5,    0, 0,        0,0,-1,
         0.5, -0.5, -0.5,    1, 0,        0,0,-1,
         0.5,  0.5, -0.5,    1, 1,        0,0,-1,
        -0.5,  0.5, -0.5,    0, 1,        0,0,-1,
       
    # X+          
         0.5, -0.5, -0.5,    0, 0,        1,0,0,
         0.5,  0.5, -0.5,    1, 0,        1,0,0,
         0.5,  0.5,  0.5,    1, 1,        1,0,0,
         0.5, -0.5,  0.5,    0, 1,        1,0,0,   
    # X-          
        -0.5, -0.5, -0.5,    0, 0,        -1,0,0,
        -0.5,  0.5, -0.5,    1, 0,        -1,0,0,
        -0.5,  0.5,  0.5,    1, 1,        -1,0,0,
        -0.5, -0.5,  0.5,    0, 1,        -1,0,0,   
    # Y+          
        -0.5,  0.5, -0.5,    0, 0,        0,1,0,
         0.5,  0.5, -0.5,    1, 0,        0,1,0,
         0.5,  0.5,  0.5,    1, 1,        0,1,0,
        -0.5,  0.5,  0.5,    0, 1,        0,1,0,   
    # Y-          
        -0.5, -0.5, -0.5,    0, 0,        0,-1,0,
         0.5, -0.5, -0.5,    1, 0,        0,-1,0,
         0.5, -0.5,  0.5,    1, 1,        0,-1,0,
        -0.5, -0.5,  0.5,    0, 1,        0,-1,0
        ]   

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices, image_filename)