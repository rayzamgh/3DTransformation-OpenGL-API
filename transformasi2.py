import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import math

from copy import deepcopy


ANIRES = 100

def vectorTransformation (vertices, dp) :
	vertices1 = deepcopy(vertices)
	for i in range(len(vertices)) :
		vertices1[i] += dp
	return vertices1

def matrixTransformation (vertices, M) :
	vertices1 = deepcopy(vertices)
	for i in range(len(vertices)) :
		vertices1[i] = np.dot(M, vertices1[i])
	return vertices1

def linearTransition (vertices1, vertices2, k) :
	vertices3 = deepcopy(vertices1)
	for i in range(len(vertices1)) :
		vertices3[i] = (1-k)*vertices1[i] + k*vertices2[i]
	return vertices3


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
			self.vertices[:] = vectorTransformation(self.vertices,dp)
			self.update()

	def dilate (self, inp):
		k = float(inp[1])
		Mp = np.array([[k, 0.0, 0.0], [0.0, k, 0.0], [0.0, 0.0, k]])
		vertices1 = deepcopy(self.vertices)
		vertices2 = matrixTransformation(self.vertices,Mp)
		for i in range(ANIRES + 1) :
			self.vertices[:] = linearTransition(vertices1,vertices2,i*1.0/ANIRES)
			self.update()
		
	def rotate (self, inp) :
		vektor = str(inp[2])
		t = np.deg2rad(float(inp[1]))
		tp = t/ANIRES
		vertices1 = deepcopy(self.vertices)
		if (len(inp) == 4) :
			a = inp[3].split(",")
			if (len(a) == 3) :
				x = a[0].split("(")
				y = a[1]
				z = a[2].split(")")
				p = float(x[1])
				q = float(y)
				r = float(z[0])
				d = np.array([p, q, r])
				di = np.array([-p, -q, -r])				
			elif (len(a) == 2) :
				x = a[0].split("(")
				y = a[1].split(")")
				p = float(x[1])
				q = float(y[0])
				d = np.array([p, q, 0.0])
				di = np.array([-p, -q, 0.0])
		elif (len(inp) == 3) :
			d = np.array([0.0, 0.0, 0.0])
			di = np.array([0.0, 0.0, 0.0])
		
		if vektor == 'z':
			Mp = np.array([[math.cos(tp), -math.sin(tp), 0.0], [math.sin(tp), math.cos(tp), 0.0], [0.0, 0.0, 1.0]])
			M = np.array([[math.cos(t), -math.sin(t), 0.0], [math.sin(t), math.cos(t), 0.0], [0.0, 0.0, 1.0]])
		elif vektor == 'y':
			Mp = np.array([[math.cos(tp), 0.0, math.sin(tp)], [0.0, 1.0, 0.0], [-math.sin(tp), 0.0, math.cos(tp)]])
			M = np.array([[math.cos(t), 0.0, math.sin(t)], [0.0, 1.0, 0.0], [-math.sin(t), 0.0, math.cos(t)]])
		elif vektor == 'x':
			Mp = np.array([[1.0 ,0.0, 0.0], [0.0, math.cos(tp), -math.sin(tp)], [0.0, math.sin(tp), math.cos(tp)]])
			M = np.array([[1.0 ,0.0, 0.0], [0.0, math.cos(t), -math.sin(t)], [0.0, math.sin(t), math.cos(t)]])
		else :
			a = vektor.split(",")
			x = a[0].split("(")
			y = a[1]
			z = a[2].split(")")
			us = np.array([float(x[1]), float(y), float(z[0])])
			lus = math.sqrt(us[0]*us[0] + us[1]*us[1] + us[2]*us[2])
			u = us/lus
			M = np.array(	[[(math.cos(t)+(u[0]*u[0])*(1 - math.cos(t))), ((u[0]*u[1])*(1 - math.cos(t)) - u[2]*math.sin(t)), ((u[0]*u[2])*(1 - math.cos(t)) + u[1]*math.sin(t))],
							[((u[1]*u[0])*(1 - math.cos(t)) + u[2]*math.sin(t)), (math.cos(t)+(u[1]*u[1])*(1 - math.cos(t))), ((u[1]*u[2])*(1 - math.cos(t)) - u[0]*math.sin(t))],
							[((u[2]*u[0])*(1 - math.cos(t)) - u[1]*math.sin(t)), ((u[2]*u[1])*(1 - math.cos(t)) + u[0]*math.sin(t)), (math.cos(t)+(u[2]*u[2])*(1 - math.cos(t)))]])
			Mp = np.array(	[[(math.cos(tp)+(u[0]*u[0])*(1 - math.cos(tp))), ((u[0]*u[1])*(1 - math.cos(tp)) - u[2]*math.sin(tp)), ((u[0]*u[2])*(1 - math.cos(tp)) + u[1]*math.sin(tp))],
							[((u[1]*u[0])*(1 - math.cos(tp)) + u[2]*math.sin(tp)), (math.cos(tp)+(u[1]*u[1])*(1 - math.cos(tp))), ((u[1]*u[2])*(1 - math.cos(tp)) - u[0]*math.sin(tp))],
							[((u[2]*u[0])*(1 - math.cos(tp)) - u[1]*math.sin(tp)), ((u[2]*u[1])*(1 - math.cos(tp)) + u[0]*math.sin(tp)), (math.cos(tp)+(u[2]*u[2])*(1 - math.cos(tp)))]])
			
		
		for i in range(ANIRES) :
			self.vertices[:] = vectorTransformation(self.vertices,di)
			self.vertices[:] = matrixTransformation(self.vertices,Mp)
			self.vertices[:] = vectorTransformation(self.vertices,d)
			self.update()

	
	def reflect (self, inp) :
		param = inp[1]
		vertices1 = deepcopy(self.vertices)
		if param == "x" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		elif param == "y" :
			Mp = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		elif ((param == "y=x") or (param == "x=y")) :
			Mp = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		elif ((param == "y=-x") or (param == "x=-y")) :
			Mp = np.array([[0.0, -1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		elif ((param == "xy-plane") or (param == "xy-plane")) :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		elif ((param == "xz-plane") or (param == "zx-plane")) :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		elif ((param == "yz-plane") or (param == "zy-plane")) :
			Mp = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices,Mp)
		else :
			a = param.split(",")
			if (len(a) == 2) :	
				x = a[0].split("(")
				y = a[1].split(")")
				p = float(x[1])
				q = float(y[0])
				d = [p, q, 0.0]
				di = [-p, -q, 0.0]
				Mp = np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])
				vertices2 = vectorTransformation(self.vertices,di)
				vertices2 = matrixTransformation(vertices2,Mp)
				vertices2 = vectorTransformation(vertices2,d)
			elif (len(a) == 3) :
				x = a[0].split("(")
				y = a[1]
				z = a[2].split(")")
				p = float(x[1])
				q = float(y)
				r = float(z[0])
				d = [p, q, r]
				di = [-p, -q, -r]
				Mp = np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]])
				vertices2 = vectorTransformation(self.vertices,di)
				vertices2 = matrixTransformation(vertices2,Mp)
				vertices2 = vectorTransformation(vertices2,d)
		for i in range(ANIRES + 1) :
			self.vertices[:] = linearTransition(vertices1,vertices2,i*1.0/ANIRES)
			self.update()
		
	
	def orthodonalProjection (self, inp) :
		param = inp[1]
		vertices1 = deepcopy(self.vertices)
		if (param == "x-axis") :
			Mp = np.array([[1.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "y-axis") :
			Mp = np.array([[0.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 0.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "z-axis") :
			Mp = np.array([[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif ((param == "xy-plane") or (param == "yx-plane")) :
			Mp = np.array([[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 0.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)	
		elif ((param == "xz-plane") or (param == "zx-plane")) :
			Mp = np.array([[1.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif ((param == "yz-plane") or (param == "zy-plane")) :
			Mp = np.array([[0.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		for i in range(ANIRES + 1) :
			self.vertices[:] = linearTransition(vertices1,vertices2,i*1.0/ANIRES)
			self.update()

	def shear (self, inp) :
		k = float(inp[1])
		param = inp[2]
		vertices1 = deepcopy(self.vertices)
		if (param == "y-x") :
			Mp = np.array([[1.0, k, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "z-x") :
			Mp = np.array([[1.0, 0.0, k],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "x-y") :
			Mp = np.array([[1.0, 0.0, 0.0],[k, 1.0, 0.0],[0.0, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "z-y") :
			Mp = np.array([[1.0, 0.0, 0.0],[0.0, 1.0, k],[0.0, 0.0, 0.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "x-z") :
			Mp = np.array([[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[k, 0.0, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		elif (param == "y-z") :
			Mp = np.array([[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, k, 1.0]])
			vertices2 = matrixTransformation(self.vertices, Mp)
		for i in range(ANIRES + 1) :
			self.vertices[:] = linearTransition(vertices1,vertices2,i*1.0/ANIRES)
			self.update()


	def stretch (self, inp) :
		param = inp[2]
		k = float(inp[1])
		vertices1 = deepcopy(self.vertices)
		if param == "x" :
			Mp = np.array([[k, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
		elif param == "y" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, k, 0.0], [0.0, 0.0, 1.0]])
		elif param == "z" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, k]])
		vertices2 = matrixTransformation(self.vertices, Mp)
		for i in range(ANIRES + 1) :
			self.vertices[:] = linearTransition(vertices1,vertices2,i*1.0/ANIRES)
			self.update()
	
	def custom (self, inp) :
		if (len(inp) == 5) :
			Mp = np.array([[float(inp[1]), float(inp[2]), 0.0], [float(inp[3]), float(inp[4]), 0.0], [0.0, 0.0, 1.0]])
		elif (len(inp) == 10) :
			Mp = np.array([[float(inp[1]), float(inp[2]), float(inp[3])], [float(inp[4]), float(inp[5]), float(inp[6])], [float(inp[7]), float(inp[8]), float(inp[9])]])
		vertices1 = deepcopy(self.vertices)
		vertices2 = matrixTransformation(self.vertices,Mp)
		for i in range(ANIRES + 1) :
			self.vertices[:] = linearTransition(vertices1,vertices2,i*1.0/ANIRES)
			self.update()


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
	print("3. Custom (2D)")


	inp = int(input())
	if (inp == 1):
		main_object = Shape([[5.0, -5.0, -5.0],	[5.0, 5.0, -5.0],	[-5.0, 5.0, -5.0], [-5.0, -5.0, -5.0], 
							[5.0, -5.0, 5.0], [5.0, 5.0, 5.0], [-5.0, -5.0, 5.0], [-5.0, 5.0, 5.0]], 
							[[0, 1], [0, 3], [0, 4], [2, 1], [2, 3], [2, 7],
							[6, 3], [6, 4], [6, 7], [5, 1], [5, 4], [5, 7]])
	elif (inp == 2):
		main_object = Shape([[5.0, 5.0, 0], [5.0, -5.0, 0], [-5.0, -5.0, 0], [-5.0, 5.0, 0]],
							[[0,1], [1,2], [2, 3], [3,0]])
	elif (inp == 3):
		Vertices = []
		Vertex = []
		Edges = []
		Edge = []
		N = int(input("Masukkan N:"))
		for i in range(N):
			Vertex = []
			Edge = []
			inp = input().split(' ')
			Vertex.append(float(inp[0]))
			Vertex.append(float(inp[1]))
			Vertex.append(0.0)
			Vertices.append(Vertex)
			Edge.append(i)
			if i == (N-1) :
				Edge.append(0)
			else :
				Edge.append(int(i+1))
			Edges.append(Edge)
			print(Edges)
			print(Edge)
			print(Vertices)
			print(Vertex)
		main_object = Shape(Vertices, Edges)
	
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
	main_object.update()
	while True:
		inp = input().split(" ")
		if (inp[0] == 'translate'):
			main_object.translate(inp)
		elif (inp[0] == 'dilate'):
			main_object.dilate(inp)
		elif (inp[0] == 'rotate'):
			main_object.rotate(inp)
		elif (inp[0] == 'reflect'):
			main_object.reflect(inp)
		elif (inp[0] == 'stretch'):
			main_object.stretch(inp)	
		elif (inp[0] == 'custom'):
			main_object.custom(inp)	
		elif (inp[0] == 'projection'):
			main_object.orthodonalProjection(inp)
		elif (inp[0] == 'shear'):
			main_object.shear(inp)
		elif (inp[0] == 'exit'):
			pygame.quit()
			quit()

		"""
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
		
			
		if ((event.type == KEYDOWN) and (event.key == K_l) ):
			inp = input().split(" ")
			if (inp[0] == 'translate'):
				main_object.translate(inp)
			elif (inp[0] == 'dilate'):
				main_object.dilate(inp)
			elif (inp[0] == 'rotate'):
				main_object.rotate(inp)
			elif (inp[0] == 'reflect'):
				main_object.reflect(inp)
			elif (inp[0] == 'stretch'):
				main_object.stretch(inp)	
			elif (inp[0] == 'custom'):
				main_object.custom(inp)	
			elif (inp[0] == 'exit'):
				pygame.quit()
				quit()
		"""
		"""
			while True:
				for event in pygame.event.get():
					pass
				if (event.type == ACTIVEEVENT and event.gain == 1):
					break	
		"""

		main_object.update()
main()