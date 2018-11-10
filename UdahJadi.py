import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class Shape:
	def __init__(self, vertices = [], edges = []):
		self.vertices = np.array(vertices)
		self.edges = np.array(edges)

	def translate(self, inp):
		if (len(inp) == 4):	
			dx = int(inp[1])
			dy = int(inp[2])
			dz = int(inp[3])
		else:
			dx = int(inp[1])
			dy = int(inp[2])
			dz = 0
		d = np.array([dx, dy, dz])
		dt = d/100
		for j in range(100):
			for i in range(len(self.vertices)):
				self.vertices[i] = self.vertices[i] + dt
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			draw(sbX)
			draw(sbY)
			draw(sbZ)
			draw(self)
			pygame.display.flip()
			pygame.time.wait(10)

	def dilate(self, inp):
		k = float(inp[1])
		M = np.array([[k, 0.0, 0.0],[0.0, k, 0.0],[0.0, 0.0, k]])
		for i in range(len(self.vertices)):
			self.vertices[i] = np.dot((M),self.vertices[i])
		
def initiate():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Tubes Algeo")
	gluPerspective(45, (display[0]/display[1]), 0.1, 200.0)
	glTranslatef(0.0, -3, -35.5)
	glRotatef(45, 1, 1, 0)
	glRotatef(15, -1, 0, 0)
	"""MENERIMA INPUT USER"""
	print("Welcome to 3D transformation simulator!")
	print("Bentuk apakah yang ingin anda tampilkan?")
	print("1. Kubus (3D)")
	print("2. Persegi (2D)")

	inp = int(input())
	if (inp == 1):
		main_object = Shape([[5.0, -5.0, -5.0],	[5.0, 5.0, -5.0],	[-5.0, 5.0, -5.0], [-5.0, -5.0, -5.0], 
							[5.0, -5.0, 5.0], [5.0, 5.0, 5.0], [-5.0, -5.0, 5.0], [-5.0, 5.0, 5.0]], 
							[[0, 1], [0, 3], [0, 4], [2, 1], [2, 3], [2, 7],
							[6, 3], [6, 4], [6, 7], [5, 1], [5, 4], [5, 7]])
	elif (inp == 2):
		main_object = Shape([[5.0, 5.0, 0], [5.0, -5.0, 0], [-5.0, -5.0, 0], [-5.0, 5.0, 0]],
							[[0,1], [1,2], [2, 3], [3,0]])

	return main_object
		
def draw(main_object = Shape()):
	glBegin(GL_LINES)
	for edge in main_object.edges:
		for vertex in edge:
			glVertex3fv(main_object.vertices[vertex])
	glEnd()

sbX = Shape([[100.0, 0.0, 0.0],[-100.0, 0.0, 0.0]], [[0, 1]])
sbY = Shape([[0.0, 100.0, 0.0],[0.0, -100.0, 0.0]], [[0, 1]])
sbZ = Shape([[0.0, 0.0, 100.0],[0.0, 0.0, -100.0]], [[0, 1]])

def main():
	main_object = initiate()
	while True:
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		for event in pygame.event.get():
			pass

		
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				glRotatef(1, 0, 1, 0)
			elif event.key == K_LEFT:
				glRotatef(1,0,-1, 0)
			elif event.key == K_UP:
				glRotatef(1,-1,0, 0)
			elif event.key == K_DOWN:
				glRotatef(1,1,0, 0)
			elif event.key == K_a:
				glRotatef(1,0,0, -1)
			elif event.key == K_d:
				glRotatef(1,0,0, 1)
			else:
				pass
		
		if (event.type == ACTIVEEVENT and event.gain == 0):
			inp = input().split(' ')
			if (inp[0] == 'translate'):
				main_object.translate(inp)
			elif (inp[0] == 'dilate'):
				main_object.dilate(inp)
			elif (inp[0] == 'exit'):
				pygame.quit()
				quit()

			while True:
				for event in pygame.event.get():
					pass
				if (event.type == ACTIVEEVENT and event.gain == 1):
					break	

		draw(sbX)
		draw(sbY)
		draw(sbZ)
		draw(main_object)
		pygame.display.flip()
		pygame.time.wait(5)

main()