# coding=utf-8
"""
tarea2b.py
Tarea 2b - Bryan Ortiz
>> Estrella de la muerte <<
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations2 as tr2
import basic_shapes as bs
import scene_graph2 as sg
import easy_shaders as es


# A class to store the application control
# Add follow_car option
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False
        self.free_camera = True
        self.camera_number = 1
        self.lights = False
        self.starBroken = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_1:
        controller.camera_number = 1
        controller.free_camera = False
        print ("[Camera #1]")

    elif key == glfw.KEY_2:
        controller.camera_number = 2
        controller.free_camera = False
        print ("[Camera #2]")

    elif key == glfw.KEY_3:
        controller.camera_number = 3
        controller.free_camera = False
        print ("[Camera #3]")

    elif key == glfw.KEY_4:
        controller.camera_number = 4
        controller.free_camera = False 
        print ("[Camera #4]")

    elif key == glfw.KEY_W or key == glfw.KEY_S or key == glfw.KEY_D or key == glfw.KEY_A:
        controller.free_camera = True  

    elif key == glfw.KEY_Q:
        print ("[ZOOM IN]")
    
    elif key == glfw.KEY_E:
        print ("[ZOOM OUT]")

    elif key == glfw.KEY_ENTER:
        controller.starBroken = not controller.starBroken

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# Create DeathStar
def createTextureDeathStar(filename):
    gpuSphere = es.toGPUShape(bs.createTextureSphere(filename), GL_MIRRORED_REPEAT, GL_NEAREST)
    gpuInside = es.toGPUShape(bs.createInsideSphere("textures/dsInside.jpg"), GL_MIRRORED_REPEAT, GL_NEAREST)
    gpuCone = es.toGPUShape(bs.createTextureCone("textures/laser.png"), GL_MIRRORED_REPEAT, GL_NEAREST)

    star_base = sg.SceneGraphNode("star_base")
    star_base.transform = tr2.scale(0.5, 0.5, 0.5)
    star_base.childs += [gpuSphere]

    star_inside = sg.SceneGraphNode("star_inside")
    star_inside.transform = tr2.scale(0.5, 0.5, 0.5)
    star_inside.childs += [gpuInside]

    star_aerial = sg.SceneGraphNode("star_aerial")
    star_aerial.transform = np.matmul(tr2.translate(0, -np.sin(3*np.pi/8)/2, np.cos(3*np.pi/8)/2) , tr2.rotationX(3*np.pi/8) )
    star_aerial.transform = np.matmul(star_aerial.transform,  tr2.scale(0.15,0.15,0.05))
    star_aerial.childs += [gpuCone]

    star = sg.SceneGraphNode("star")
    star.transform = tr2.rotationY(np.pi/32)
    star.childs += [star_inside, star_base, star_aerial] 

    return star

# Create Earth with textures
def createEarth():
    gpuEarth_texture = es.toGPUShape(bs.createTextureQuad("textures/earth.png"), GL_REPEAT, GL_NEAREST)
    earth_scaled = sg.SceneGraphNode("earth_scaled")
    earth_scaled.transform = tr2.scale(0.5, 0.5, 0.5)
    earth_scaled.childs += [gpuEarth_texture]

    earth_rotated = sg.SceneGraphNode("earth_rotated_x")
    earth_rotated.transform = tr2.rotationX(np.pi/2)
    earth_rotated.childs += [earth_scaled]

    earth = sg.SceneGraphNode("earth")
    earth.transform = tr2.translate(0.5, 4, 0.6)
    earth.childs += [earth_rotated]

    return earth

# Create ambient box
def createBox(filename):
    gpuCube = es.toGPUShape(bs.createTextureCube(filename), GL_MIRRORED_REPEAT, GL_NEAREST)
    bgCube_scaled = sg.SceneGraphNode("bgCube_scaled")
    bgCube_scaled.transform = tr2.scale(9, 9, 9)
    bgCube_scaled.childs += [gpuCube]

    bgCube = sg.SceneGraphNode("bgCube_scaled")
    bgCube.transform = tr2.translate(0, 0, 0)
    bgCube.childs += [bgCube_scaled]

    return bgCube

# Create spaceship
def createSpaceShip():
    gpuCenterShip = es.toGPUShape(bs.createTextureSphere("textures/ssCenter.jpg"), GL_MIRRORED_REPEAT , GL_NEAREST)
    gpuBlock = es.toGPUShape(bs.createTextureCube("textures/ssBlock.jpg"), GL_REPEAT , GL_NEAREST)
    gpuPlane = es.toGPUShape(bs.createTextureHex("textures/ssWings.jpg"),GL_REPEAT,GL_NEAREST)
    
    spaceShipCenter = sg.SceneGraphNode("spaceShipCenter")
    spaceShipCenter.transform = tr2.scale(0.1, 0.1, 0.1 )
    spaceShipCenter.childs += [gpuCenterShip]

    spaceShipBlock = sg.SceneGraphNode("spaceShipBlock")
    spaceShipBlock.transform = tr2.scale(0.02, 0.4, 0.02 )
    spaceShipBlock.childs += [gpuBlock]

    spaceShipWingL = sg.SceneGraphNode("spaceShipLeftWing")
    spaceShipWingL.transform = np.matmul (tr2.translate(0.02,-0.2,0.02), np.matmul(tr2.rotationX(np.pi/2), tr2.scale(0.3,0.3,0.3)))
    spaceShipWingL.childs += [gpuPlane]

    spaceShipWingR = sg.SceneGraphNode("spaceShipRightWing")
    spaceShipWingR.transform = np.matmul (tr2.translate(0.02,0.2,0.02), np.matmul(tr2.rotationX(np.pi/2), tr2.scale(0.3,0.3,0.3)))
    spaceShipWingR.childs += [gpuPlane]

    spaceShip_rotated = sg.SceneGraphNode("spaceShip_rotated")
    spaceShip_rotated.transform = np.matmul(tr2.rotationZ(0), tr2.rotationY(np.pi/ 2 ))
    spaceShip_rotated.childs += [spaceShipCenter, spaceShipBlock, spaceShipWingR, spaceShipWingL]

    spaceShip_scaled = sg.SceneGraphNode("spaceShip_scaled")
    spaceShip_scaled.transform = tr2.scale(0.5, 0.5, 0.5)
    spaceShip_scaled.childs += [ spaceShip_rotated ]

    spaceShip = sg.SceneGraphNode("spaceShip")
    spaceShip.transform = tr2.translate(0, 0, 0)
    spaceShip.childs += [ spaceShip_scaled ]

    return spaceShip


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 700
    height = 700

    window = glfw.create_window(width, height, "Tarea 2 - DeathStar", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with shaders (simple, texture and lights)
    mvcPipeline = es.SimpleModelViewProjectionShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    phongPipeline = es.SimplePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(1, 1, 1, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST) 

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    earthNode = createEarth()
    shipNode1 = createSpaceShip()
    shipNode2 = createSpaceShip()
    bgBoxNode = createBox("textures/bg.jpg")
    starCompleteNode = createTextureDeathStar("textures/superDS.png")
    starBrokenNode = createTextureDeathStar("textures/dsBroken.png")

    # Define radius of the circumference
    r = 2
    t0 = glfw.get_time()
    camera_theta = 3*np.pi/4
    camera_phi = np.pi/2
    distance = 2/np.sin(camera_theta)

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Telling OpenGL to use our shader program
        glUseProgram(mvcPipeline.shaderProgram)
       
        # Using the same view and projection matrices in the whole application
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)
        glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        if controller.starBroken:
            starNode = starCompleteNode
        else:
            starNode = starBrokenNode

        
        if not controller.free_camera:
            if controller.camera_number == 1:
                # static camera
                normal_view = tr2.lookAt(
                np.array([2, 2, -1]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
                )
            elif controller.camera_number == 2:
                # static camera
                normal_view = tr2.lookAt(
                np.array([2, -2, 0]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
                )
            elif controller.camera_number == 3:
                # static camera
                normal_view = tr2.lookAt(
                np.array([1, 1, 3]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
                )
            else:
                # static camera
                normal_view = tr2.lookAt(
                np.array([-2, -2, 1]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
                )
        else:

            if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
                camera_theta -= dt

            if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
                camera_theta += dt

            if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS and camera_phi > 0):
                camera_phi -= dt

            if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS and camera_phi < np.pi):
                camera_phi += dt

            if (glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS and distance > 0.8):
                distance -= 2* dt

            if (glfw.get_key(window, glfw.KEY_E) == glfw.PRESS and distance < 4):
                distance += 2* dt

            # Setting up the view transform
            camX = distance * np.sin(camera_theta) * np.sin(camera_phi)
            camY = distance * np.cos(camera_theta) * np.sin(camera_phi)
            camZ = distance * np.cos(camera_phi)

            eye = np.array([camX, camY, camZ])
            at = np.array([0, 0, 0]) # Centro (0,0,0)
            up = np.array([0, 0, np.sin(camera_phi)])

            normal_view = tr2.lookAt(eye,at,up)

        # Calculate coordinates of the camera and spaceShip
        u_px = np.cos(glfw.get_time())
        u_py = np.sin(glfw.get_time())
        x = r * u_px
        y = r * u_py

        glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "view"), 1, GL_TRUE, normal_view)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if controller.showAxis:
            glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "model"), 1, GL_TRUE, tr2.identity())
            mvcPipeline.drawShape(gpuAxis, GL_LINES)

        # Moving the spaceship
        shipNode1.transform = tr2.translate(x+0.8, y+0.8, 0)
        shipNode1.transform = np.matmul(shipNode1.transform, tr2.rotationZ(glfw.get_time() + np.pi / 2))

        shipNode2.transform = tr2.translate(-x+2, y-1, 1.5)
        shipNode2.transform = np.matmul(shipNode2.transform, tr2.rotationZ(-glfw.get_time() + np.pi / 2))

        # Drawing the scene
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, normal_view)
        

        # Box, Earth and deathstar
        sg.drawSceneGraphNode(bgBoxNode, textureShaderProgram)
        sg.drawSceneGraphNode(earthNode, textureShaderProgram)
        sg.drawSceneGraphNode(starNode, textureShaderProgram)
       
        # Drawing the ship
        sg.drawSceneGraphNode(shipNode1, textureShaderProgram)
        sg.drawSceneGraphNode(shipNode2, textureShaderProgram)

        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()