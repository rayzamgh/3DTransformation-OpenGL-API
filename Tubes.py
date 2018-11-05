import pygame
import numpy as np
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
	(1, -1, -1),
	(1, 1, -1),
	(-1, 1, -1),
	(-1, -1, -1),
	(1, -1, 1),
	(1, 1, 1),
	(-1, -1, 1),
	(-1, 1, 1),
	)

edges = (
	(0,1),
	(0,3),
	(0,4),
	(2,1),
	(2,3),
	(2,7),
	(6,3),
	(6,4),
	(6,7),
	(5,1),
	(5,4),
	(5,7),
	)

jancuks = (
	(1,1,0),
	(-1,1,0),
	(1,-1,0),
	(-1,-1,0),
	)

goblg = (
	(0,1),
	(0,2),
	(3,1),
	(3,2),
	)

def Kotak():
	glBegin(GL_LINES)
	for gobl in goblg:
		for jancuk in gobl:
			glVertex3fv(jancuks[jancuk])
	glEnd()


def Cube():
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(verticies[vertex])
	glEnd()

def Line(xa,ya,za,xb,yb,zb):
	glBegin(GL_LINES)
	glVertex3f(xa,ya,za)
	glVertex3f(xb,yb,zb)
	glEnd()



def main():
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	gluPerspective(50, (display[0]/display[1]), 0.1, 50.0)

	glTranslatef(0.0,0.0,-6)
	
	glRotatef(0,0,0,0)

	while True:
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Line(0,10,0,0,-10,0)
		Line(10,0,0,-10,0,0)
		Line(0,0,10,0,0,-10)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				glRotatef(1,0,5, 0)

			if event.key == K_LEFT:
				glRotatef(1,0,-5, 0)

			if event.key == K_UP:
				glRotatef(1,-5,0, 0)

			if event.key == K_DOWN:
				glRotatef(1,5,0, 0)

			if event.key == K_a:
				glRotatef(1,0,0, -5)

			if event.key == K_s:
				glRotatef(1,0,0, 5)


		
		Cube()
		pygame.display.flip()
		pygame.time.wait(10)
					
main()