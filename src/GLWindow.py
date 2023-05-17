import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from pyrr import Matrix44, Vector3

from Geometry import Geometry

class Triangle:

    def __init__(self, shader):
        self.vertexLoc = glGetAttribLocation(shader, "position")
        self.vertices = np.array([0.0, 0.5, 0.0,
                                  -0.5, -0.5, 0.0,
                                  0.5, -0.5, 0.0], dtype=np.float32)

        self.vertexCount = 3
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(self.vertexLoc)
        glVertexAttribPointer(self.vertexLoc, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    def cleanup(self):
        glDeleteBuffers(1, (self.vbo,))


class OpenGLWindow:
    
    def __init__(self):
        self.geo = None
        self.model = Matrix44.identity()
        self.lightModels = [Matrix44.identity(), Matrix44.identity()] # Store light model matrices
        self.viewPos = Vector3([0.0, 0.0, 4.0])
        self.view = Matrix44.look_at(self.viewPos,Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]))
        self.clock = pg.time.Clock()
        self.transformations = [] # Keeps track of the current transformations
        self.camAngle = 0  # Starting camera angle
        self.lightAngle = 0 # Starting light angle
        self.colourGrad = 0 # Colour gradient value
        self.orbiting = False # Light orbiting flag
        self.colourCycle = False # Light colour cycle flag
        self.scale = Matrix44.from_scale(Vector3([0.2, 0.2, 0.2])) # Scales down the models for the lights
        self.textureFrames = [] # List of all frames for the animated texture

    def loadShaderProgram(self, vertex, fragment):
        with open(vertex, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader

    def initGL(self, screen_width=640, screen_height=480):
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 2)

        pg.display.set_mode((screen_width, screen_height), pg.OPENGL | pg.DOUBLEBUF)

        glEnable(GL_DEPTH_TEST)

        # Uncomment these two lines when perspective camera has been implemented
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glClearColor(0, 0, 0, 1)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Sets the camera projection (fov, aspect ratio, near clipping plane and far clipping plane)
        camProjection = Matrix44.perspective_projection(45.0, screen_width / screen_height, 0.1, 100.0)
        
        self.shader = self.loadShaderProgram("./shaders/simple.vert", "./shaders/simple.frag")
        glUseProgram(self.shader)
        colourLoc = glGetUniformLocation(self.shader, "objectColour")
        glUniform3f(colourLoc, 1.0, 1.0, 1.0)
        modelLoc = glGetUniformLocation(self.shader, "Model")
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, self.model)
        viewLoc = glGetUniformLocation(self.shader, "View")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, self.view)
        projectionLoc = glGetUniformLocation(self.shader, "Projection")
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, camProjection)
        viewPosLoc = glGetUniformLocation(self.shader, "viewPosition")
        glUniform3fv(viewPosLoc, 1 ,self.viewPos) # Camera view
        
        # First light colour and position
        firstLightPosition = glGetUniformLocation(self.shader, "firstLightPosition")
        glUniform3f(firstLightPosition, 10.0, 4.0, 0.0)  # First light position
        firstLightColour = glGetUniformLocation(self.shader, "firstLightColour")
        glUniform3f(firstLightColour, 0.5, 0.0, 0.5)  # First light's colour

        # Second light colour and position
        secondLightPosition = glGetUniformLocation(self.shader, "secondLightPosition")
        glUniform3f(secondLightPosition, -10.0, -4.0, 0.0)  # Second light position
        secondLightColour = glGetUniformLocation(self.shader, "secondLightColour")
        glUniform3f(secondLightColour, 1.0, 0.0, 0.0)  # Second light's colour

        self.setupTexture() # loads in and sets up the texture image
        
        # Loads first model
        self.geo = Geometry('./resources/ball.obj')
        print("Setup complete!")

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)  # You may not need this line
        modelLoc = glGetUniformLocation(self.shader, "Model")
        viewLoc = glGetUniformLocation(self.shader, "View")
        viewPosLoc = glGetUniformLocation(self.shader, "viewPosition")        
    
        current_time = pg.time.get_ticks()
        frame_duration = 100  # Show ing each frame for 100ms
        current_frame = (current_time // frame_duration) % len(self.textureFrames)
        glBindTexture(GL_TEXTURE_2D, self.textureFrames[current_frame]) # Binding the current frame 
    
        # Renders first model
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, self.model)
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, self.view)
        glDrawArrays(GL_TRIANGLES, 0, self.geo.vertexCount)
        
        # Renders the light models
        for i in range(2):
            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, self.lightModels[i])
            glDrawArrays(GL_TRIANGLES, 0, self.geo.vertexCount)
        
        self.lightOrbit(self.orbiting, False) # Updating the light positions
        self.lightColour(self.colourCycle, False) # Updating the light colours
        glUniform3fv(viewPosLoc, 1 ,self.viewPos) # Updating the view
        
        pg.display.flip()
    
    def setupTexture(self):
        animatedTex = pg.image.load("./resources/lines.jpg")
        # animatedTex is a 480 x 22560 image that contains 47 frames of 480x480 images
        frameWidth = 480 
        frameHeight = 480
        rows = 47 
        columns = 1

        for r in range(rows):
            for c in range(columns):
                # Calculate the position of the current frame in the image
                x = c * frameWidth
                y = r * frameHeight

                # Create a surface for the frame and copy frame onto it
                frame = pg.Surface((frameWidth, frameHeight), pg.SRCALPHA)
                frame.blit(animatedTex, (0, 0), (x, y, frameWidth, frameHeight))
                textureData = pg.image.tostring(frame, "RGB", 1) # Create texture the surface
                
                texture = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, frameWidth, frameHeight, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
                self.textureFrames.append(texture)


    def lightColour(self, gradient, reset): # Changes the colour of the lights
        if(reset == True):
            # First light colour
            firstLightColour = glGetUniformLocation(self.shader, "firstLightColour")
            glUniform3f(firstLightColour, 0.5, 0.0, 0.5)
            
            # Second light colour
            secondLightColour = glGetUniformLocation(self.shader, "secondLightColour")
            glUniform3f(secondLightColour, 1.0, 0.0, 0.0)
            self.colourCycle = False
        else:
            self.colourCycle = False if gradient == False else True
            if(self.colourCycle == True): 
                self.colourGrad = self.colourGrad + 0.00005 # Increment the colour gradient
                
                # Increment the colour rgb values for the first light
                red = (np.sin(self.colourGrad * 2 * np.pi) + 1.0) / 2.0
                green = (np.sin(self.colourGrad * 2 * np.pi + 2 * np.pi / 3) + 1.0) / 2.0
                blue = (np.sin(self.colourGrad * 2 * np.pi + 4 * np.pi / 3) + 1.0) / 2.0
                firstLightColour = glGetUniformLocation(self.shader, "firstLightColour")
                glUniform3f(firstLightColour, red, green, blue)
                
                # Increment the colour rgb values for the second light
                red = (np.sin((self.colourGrad + 0.5) * 2 * np.pi) + 1.0) / 2.0
                green = (np.sin((self.colourGrad + 0.5) * 2 * np.pi + 2 * np.pi / 3) + 1.0) / 2.0
                blue = (np.sin((self.colourGrad + 0.5) * 2 * np.pi + 4 * np.pi / 3) + 1.0) / 2.0
                secondLightColour = glGetUniformLocation(self.shader, "secondLightColour")
                glUniform3f(secondLightColour, red, green, blue)

    def lightOrbit(self, orbit, reset):
        if(reset == True):
            # Reset light positions
            firstLightPosition = glGetUniformLocation(self.shader, "firstLightPosition")
            glUniform3f(firstLightPosition, 10.0, 4.0, 0.0)  # First light position
            self.lightModels[0] = Matrix44.from_translation(Vector3([10.0, 4.0, 0.0])) * self.scale
            
            secondLightPosition = glGetUniformLocation(self.shader, "secondLightPosition")
            glUniform3f(secondLightPosition, -10.0, -4.0, 0.0)  # Second light position
            self.lightModels[1] = Matrix44.from_translation(Vector3([-10.0, -4.0, 0.0])) * self.scale
            self.orbiting = False  # Lights stop orbiting
        else:
            self.orbiting = False if orbit == False else True
            if(self.orbiting == True): 
                self.lightAngle = self.lightAngle + (0.01) # Increments the angle for the light
                # Updates the x and z coords for the first light
                x = 10.0 * np.cos(np.radians(self.lightAngle)) 
                z = 10.0 * np.sin(np.radians(self.lightAngle))
                firstLightPosition = glGetUniformLocation(self.shader, "firstLightPosition")
                glUniform3f(firstLightPosition, x, 4.0, z)  # Update first light position
                self.lightModels[0] = Matrix44.from_translation(Vector3([x, 4.0, z])) * self.scale # Updates the first light model
                
                # Updates the x and z coords for the second light
                x = -10.0 * np.cos(-np.radians(self.lightAngle))
                z = -10.0 * np.sin(-np.radians(self.lightAngle))
                secondLightPosition = glGetUniformLocation(self.shader, "secondLightPosition")
                glUniform3f(secondLightPosition, x, -4.0, z)  # Update second light position
                self.lightModels[1] = Matrix44.from_translation(Vector3([x, -4.0, z])) * self.scale # Updates the second light model

    def camRotate(self, val): # Rotates the camera around the model
        if(val > 0): # Rotate uniformly if input is positive
            self.camAngle = self.camAngle + 5
        if(val < 0):  # Rotate uniformly if input is negative
            self.camAngle = self.camAngle - 5
        # Updating z and x positions
        x = 4 * np.sin(np.radians(self.camAngle))
        z = 4 * np.cos(np.radians(self.camAngle))
        self.viewPos = Vector3([x, 0.0, z]) 
        self.view = Matrix44.look_at(self.viewPos, Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]))

    def rotate(self, val, axis): # Rotates the model
        if(val > 0): # Rotate uniformly if input is positive
            rotate = 15
        if(val < 0):  # Rotate uniformly if input is negative
            rotate = -15
            
        if(axis == 1): # Rotates the model on its selected axis
            rotationMatrix = Matrix44.from_x_rotation((np.radians(rotate)), dtype=np.float32)
        elif(axis == 2):
            rotationMatrix = Matrix44.from_y_rotation((np.radians(rotate)), dtype=np.float32)
        elif(axis == 3):
            rotationMatrix = Matrix44.from_z_rotation((np.radians(rotate)), dtype=np.float32)
        self.transformations.insert(0, rotationMatrix)
        self.applyTransformations()

    def scaleModel(self, val, axis): #Scales the model
        if(val > 0): # Scale up uniformly if input is positive
            scaleVal = 1.1
        if(val < 0):  # Scale down uniformly if input is negative
            scaleVal = 1/1.1
            
        if(axis == 1): # Scales the model on its selected axis
            scaleMatrix =  Matrix44.from_scale(Vector3([scaleVal, 1.0, 1.0]))
        elif(axis == 2):
            scaleMatrix =  Matrix44.from_scale(Vector3([1.0, scaleVal, 1.0]))
        elif(axis == 3):
            scaleMatrix =  Matrix44.from_scale(Vector3([1.0, 1.0, scaleVal]))
        self.transformations.append(scaleMatrix)
        self.applyTransformations()

    def applyTransformations(self):
        self.model = Matrix44.identity() # Resets the first model
        for transformation in self.transformations: # Applies the transformations
            self.model = self.model * transformation

    def resetTransformations(self):
        self.model = Matrix44.identity() # Resets the first model
        self.view = Matrix44.look_at(Vector3([0.0, 0.0, 4.0]),Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0])) # Resets the camera view
        self.viewPos = Vector3([0.0, 0.0, 4.0])
        self.view = Matrix44.look_at(self.viewPos, Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]))
        self.transformations.clear() # Clears the translation list
        self.lightOrbit(False, True) # Resets the lights back to default
        self.lightColour(False, True) # Resets colour to default
        self.lightAngle = 0
        self.colourGrad = 0
        self.camAngle = 0

    def cleanup(self):
        glDeleteVertexArrays(1, (self.vao,))
        self.geo.cleanup() 
