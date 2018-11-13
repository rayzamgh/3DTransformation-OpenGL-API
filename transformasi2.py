import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import math

from copy import deepcopy


ANIRES = 100


class Shape:
	def __init__(self, vertices = [], edges = []):
		self.vertices = np.array(vertices)
		self.edges = np.array(edges)
	

	def update (self) :
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		draw(sbX)
		draw(sbY)
		draw(sbZ)
		draw(self)
		pygame.display.flip()
		pygame.time.wait(10)

	
	def vectorTransformation (self, dp) :
		shape1 = deepcopy(self)
		for i in range(len(self.vertices)) :
			shape1.vertices[i] += dp
		return shape1
	
	def matrixTransformation (self, M) :
		shape1 = deepcopy(self)
		for i in range(len(self.vertices)) :
			shape1.vertices[i] = np.dot(M, self.vertices[i])
		return shape1
	
	def linearTransition (self, shape1, k) :
		shape2 = deepcopy(self)
		for i in range(len(self.vertices)) :
			shape2.vertices[i] = (1-k)*self.vertices[i] + k*shape1.vertices[i]
		return shape2

	def translate (self, inp):
		if len(inp) == 4 :	
			dx = float(inp[1])
			dy = float(inp[2])
			dz = float(inp[3])
		elif len(inp) == 3 :
			dx = float(inp[1])
			dy = float(inp[2])
			dz = 0
		d = np.array([dx, dy, dz])
		dp = d/ANIRES
		for i in range(ANIRES) :
			self = vectorTransformation(self,dp)
			update(self)

	'''
	def dilate (self, inp):
		k = float(inp[1])
		kp = math.pow(k,1/ANIRES)
		Mp = np.array([[kp, 0.0, 0.0], [0.0, kp, 0.0], [0.0, 0.0, kp]])
		shape1 = deepcopy(self)
		shape2 = matrixTransformation(self,Mp)
		for i in range(ANIRES) :
			self = linearTransition(shape1,shape2,i*1.0/ANIRES)
			update(self)
		
	def rotate (self, inp) :
		t = float(inp[1])
		tp = theta/ANIRES
		Mp = np.array([math.cos(tp), -math.sin(tp), 0.0], [math.sin(tp), math.cos(tp), 0.0], [0.0, 0.0, 1.0])
		for i in range(ANIRES) :
			matrixTransformation(self,Mp)
			update(self)
	
	def reflect (self, inp) :
		param = inp[1]
		shape1 = deepcopy(self)
		if param == "x" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = matrixTransformation(self,Mp)
		elif param == "y" :
			Mp = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = matrixTransformation(self,Mp)
		elif param == "y=x" :
			Mp = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = matrixTransformation(self,Mp)
		elif param == "y=-x" :
			Mp = np.array([[0.0, -1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = matrixTransformation(self,Mp)
		else :
			a = param.split(",")
			x = a[0].split("(")
			y = a[1].split(")")
			p = float(x[0])
			q = float(y[0])
			d = [p, q, 0.0]
			Mp = np.array([-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0])
			shape2 = vectorTransformation(self,-d)
			shape2 = matrixTransformation(shape2,Mp)
			shape2 = vectorTransformation(shape2,d)
		for i in range(ANIRES) :
			self = linearTransition(shape1,shape2,i*1.0/ANIRES)
			update(self)
		
	
	def stretch (self, inp) :
		param = inp[1]
		k = float(inp[2])
		shape1 = deepcopy(self)
		if param == "x" :
			Mp = np.array([[k, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
		elif param == "y" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, k, 0.0], [0.0, 0.0, 1.0]])
		elif param == "z" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, k]])
		shape2 = matrixTransformation(self,Mp)
		for i in range(ANIRES) :
			self = linearTransition(shape1,shape2,i*1.0/ANIRES)
			update(self)
	
	def costum (self, inp) :
		param = inp[1]
		a = float(inp[2])
		b = float(inp[3])
		c = float(inp[4])
		d = float(inp[5])
		shape1 = deepcopy(self)
		Mp = np.array([[a, b, 0.0], [c, d, 0.0], [0.0, 0.0, 1.0]])
		shape2 = matrixTransformation(shape1,Mp)
		for i in range(ANIRES) :
			self = linearTransition(shape1, shape2, i*1.0/ANIRES)
			update(self)
	'''



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
			inp = input().split(" ")
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