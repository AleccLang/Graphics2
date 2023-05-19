import pygame as pg
from GLWindow import *
from OpenGL.GL import *

def main():
	""" The main method where we create and setup our PyGame program """
	running = True
	
	win =  OpenGLWindow()
	win.initGL()
	
	key = 0	# 'key' denotes whether it is rotate (r), scale (s), camera orbit (c), reset (l) or quit (q)
	axis = 0 # Denotes the x, y or z axis
	value = 0 # Denotes a step for rotation, scale
	orbit = False # To set the orbiting of the light sources
	gradient = False
 
	while running:
		for event in pg.event.get(): # Grab all of the input events detected by PyGame
			if event.type == pg.QUIT:  # This event triggers when the window is closed
				running = False
			if event.type == pg.KEYDOWN:
				if key == 0 and event.key != pg.K_MINUS and event.key != pg.K_EQUALS and event.key != pg.K_o and event.key != pg.K_v:
					key = event.key # 'key' denotes whether it is rotate (r), scale (s) or quit (q)
      
				if event.key == pg.K_x: # sets the x axis
					axis = 1
					print("x-axis")
     
				if event.key == pg.K_y: # sets the y axis
					axis = 2
					print("y-axis")
     
				if event.key == pg.K_z: # sets the z axis
					axis = 3
					print("z-axis")
     
				if event.key == pg.K_RETURN: # Clears the 'key' settings once a user clicks 'enter'
					key = 0
					axis = 0
					print("Clear settings")

				if event.key == pg.K_q:  # This event triggers when the q key is pressed down
					print("Quit")
					running = False
				
				if event.key == pg.K_MINUS: # This is used to adjust the rotation and scaling negatively
					value = -1
				
				if event.key == pg.K_EQUALS: # This is used to adjust the rotation and scaling positively
					value = 1

				if event.key == pg.K_v: # This is used to cycle the colours of the light sources
					gradient = True if gradient == False else False
					win.lightColour(gradient, False)	
     
				if event.key == pg.K_o: # This is used to set the lights to orbit around the model
					orbit = True if orbit == False else False
					win.lightOrbit(orbit, False)
    
				if key == pg.K_r and value != 0 and axis != 0:  # This event triggers when the 'r' has been selected, an axis is chosen and + or - has been pressed
					print("Rotate")
					win.rotate(value, axis)
     
				if key == pg.K_c and value != 0:  # This event triggers when the 'c' has been selected and + or - has been pressed
					print("Camera Rotate")
					win.camRotate(value)
     
				if key == pg.K_s and value != 0 and axis != 0:  # This event triggers when the 's' key has been selected, an axis is chosen and + or - has been pressed
					print("Scale")
					win.scaleModel(value, axis)
     
				if event.key == pg.K_l: # This event triggers when the 'l' key has been selected. It will reset the object to the origin
					print("Reset")
					key = 0
					axis = 0
					orbit = False
					gradient = False
					win.resetTransformations()
     
				value = 0
		win.render()
	win.cleanup()
	pg.quit()


if __name__ == "__main__":
	main()