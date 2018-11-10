import numpy as np

class Point :
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, _x, _y, _z) :
        self.x = _x
        self.y = _y
        self.z = _z

    def translate (self, dx, dy, dz) :
        self.x += dx
        self.y += dy
        self.z += dz

    def dilate (self, k) :
        self.x *= k
        self.y *= k
        self.z *= k

    def rotate2D (self, theta, a, b) :
        self.x -= a
        self.y -= b
        _x = self.x
        _y = self.y
        self.x = cos(theta)*_x - sin(theta)*_y
        self.y = sin(theta)*_x + cos(theta)*_y
        self.x += a
        self.y += b
    
    def reflect2D (self, param) :
        if param == "x" :
            self.y *= -1
        elif param == "y" :
            self.x *= -1
        elif param == "y=x" :
            temp = self.x
            self.x = self.y
            self.y = temp
        elif param == "y=-x" :
            temp = self.x
            self.x = -self.y
            self.y = -temp
        else :
            a,b = param.split(",")
            a = a.split("(")
            b = b.split(")")
            self.x = a-self.x
            self.y = b-self.y
    
    def stretch (self, param, k) :
        if param == "x" :
            self.x *= k
        elif param == "y" :
            self.y *= k
        elif param == "z" :
            self.z *= k
    
    def costum (self, a, b, c, d) :
        _x = self.x
        _y = self.y
        self.x = a*x + b*y
        self.y = c*x + d*y
    