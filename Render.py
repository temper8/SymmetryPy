import math
import aggdraw
import random
import timeit
import time
#import cairo
import numpy as np
from benchmark import exec_time

from PIL import Image, ImageDraw, ImageTk
#from cairo import ImageSurface, Context, FORMAT_ARGB32
from math import sin, cos, pi
#from shapely.geometry import LineString

def avg_clr(c1, c2, d, alpha):
	r = int(c1[0]*(1-d) + c2[0]*d)
	g = int(c1[1]*(1-d) + c2[1]*d)
	b = int(c1[2]*(1-d) + c2[2]*d)
	return int.from_bytes(bytearray([r,g,b,alpha]), "big") 

def GeneratePalette2(colors, clr_num):
	N = (clr_num+30) * 200
	pal = np.zeros(N, dtype=np.uint32)
	for i in range(0, clr_num):
		c1 = colors[i]
		c2 = colors[(i+1)%clr_num]
		for j in range(0, 200):
			d = float(j)/200
			pal[i*200+j] = avg_clr(c1,c2,d,225)
	return pal		

@exec_time()
def SymmetryWall(parameters, palette):
	w = parameters["Width"]
	h = parameters["Height"]
	r = parameters["Radius"]['value']
	t = parameters["Time"]['value']
	shift = math.pi * parameters["Shift"]['value']
	#M = vars["M"].get()
	#K = vars["K"].get()
	#K1 = vars["K1"].get()
	#K2 = vars["K2"].get()
	#pim = Image.new('RGBA', (w, h), (0, 0, 0, 255))

	X = np.linspace(0, r*np.pi, w)
	Y = np.linspace(0, r*np.pi*h/w, h)
	x, y = np.meshgrid(X, Y)
	Z = W(0, 1, x, y)*cos(2*np.pi*t) + W(2, 1, x, y)*sin(2*np.pi*t) + W(3, 2, x, y)*sin(4*np.pi*t)

	clr_num = len(palette)-1
	print(clr_num)
	Re = (np.abs(Z) + 1.5)/3
	Im = (np.angle(Z)/np.pi + 1)/2
	#print(np.amax(A))
	#U = (clr_num*Re).astype(int)
	V = (clr_num*Im).astype(int)

	#pal = GeneratePalette2(colors, clr_num)

	pim = Image.fromarray(palette[V], 'RGBA')
	return pim

def E(n, m, x, y):
	return np.exp(1j*(n*(x + y/ np.sqrt(3)) + m*2*y/ np.sqrt(3)))

def W(n, m, x, y):
	nm = n + m
	return  (E(n,m,x,y) + E(m,-nm,x,y) + E(-nm,n,x,y))/3



def Sym3(x, y, t = 0):
	#x = xy[0]
	#y = xy[1]
	x3 = x * math.sqrt(3)/2
	u = (cos(y) + cos(-x3-y/2+t) + cos(x3-y/2))/3
	v = (sin(y) + sin(-x3-y/2+t) + sin(x3-y/2))/3
	return (u,v)


def FF(z, t, k = 3, k1 = -5, k2 = 17):
	l =  0.5
	a =  0.4*sin(2*pi*t)
	b =  0.4*cos(2*pi*t)
	u = 0.4*cos(k*z) + a*cos(k1*z+2*pi*t) + b*cos(k2*z-2*pi*t) 
	v = 0.4*sin(k*z) + a*sin(k1*z+2*pi*t) + b*sin(k2*z-2*pi*t) 
	#(x,y) = (u,v)
	return (u,v)

def GeneratePalette(COLORS_NUMBER):
	bi = 64.0/256
	Colors = []
	for i in range(0, COLORS_NUMBER):
		alpha = 30
		r = (random.random()*(1.0 - bi) + bi)
		g = (random.random()*(1.0 - bi) + bi)
		b = (random.random()*(1.0 - bi) + bi)
		m = 1 #max([r,g,b])
		#print(m)
		r = int(r/m*256)
		g = int(g/m*256)
		b = int(b/m*256)
		# print(r,g,b)
		Colors.append((r, g, b))
	return Colors		


class Spiro:

	COLORS_NUMBER = 4
	Pens = []
	Colors = []

	def GeneratePalette(self):
		bi = 64.0/256
		self.Colors = []
		for i in range(0, self.COLORS_NUMBER):
			alpha = 30
			r = (random.random()*(1.0 - bi) + bi)
			g = (random.random()*(1.0 - bi) + bi)
			b = (random.random()*(1.0 - bi) + bi)
			m = 1 #max([r,g,b])
			print(m)
			r = int(r/m*256)
			g = int(g/m*256)
			b = int(b/m*256)
			# print(r,g,b)
			self.Colors.append((r, g, b))
			self.Pens.append(aggdraw.Pen((r, g, b), 0.5, alpha))


	def __init__(self, parameters):
		self.width = parameters["Width"]
		self.height = parameters["Height"]
		self.radius = parameters["Radius"]
		self.GeneratePalette()

	def RenderCairo(self, t):
		self.surface = ImageSurface(FORMAT_ARGB32, self.width, self.height)
		self.context = Context(self.surface)
		# Draw something
		self.t = t
		tt = 1.5*t
		M =1000
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,tt), self.FF(z + 1.5*math.pi,tt)] for z in Z)
		self.draw_cr_test()
		self.draw_cr_polygons(lines)
		#self.draw_cr_polygons_triangle(lines)
		#self.draw_cr_lines(lines)
		self.context.fill()
		pim = Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data(), "raw", "RGBA", 0, 1)
		return pim

	def Render(self, t):
		self.t = t
		pim = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 64))
		self.drw = aggdraw.Draw(pim)
		M = 400
		for i in range(0, int(M)):
			z =2*math.pi*i/M
			xy0 = self.FF(z,t)
			xy1 = self.FF(z + math.pi, t)
			self.draw_line(xy0, xy1)
		self.drw.flush()
		return pim

	def RenderMap(self, t):
		self.t = t
		tt = 1.5*t
		pim = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 64))
		self.drw = aggdraw.Draw(pim)
		self.drw.setantialias(True)
		M = 5000
		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = ([self.FF(z,tt), self.FF(z + 1.5*math.pi,tt)] for z in Z)
		#lines = map(lambda z:[self.Simple(z,t), self.Simple(z + math.pi/2,t)], Z)
		#lines = map(lambda z:[self.Rect(z,t), self.Rect(-z,t)], Z)
		self.draw_lines(lines)
		#self.draw_polygons(lines)
		self.drw.flush()
		return pim

	def Render2(self, vars):
		renderType = vars["RenderType"].get()
		t = 1.0*vars["Time"].get()
		shift = math.pi * vars["Shift"].get()
		M = vars["M"].get()
		K = vars["K"].get()
		K1 = vars["K1"].get()
		K2 = vars["K2"].get()
		pim = Image.new('RGBA', (self.width, self.height), (0, 0, 64, 255))
		self.drw = aggdraw.Draw(pim)
		self.drw.setantialias(True)

		Z = (2*math.pi*i/M for i in range(0, int(M)))
		lines = list([self.FF(z, t, K, K1, K2), self.FF(z + shift, t, K, K1, K2), self.GetColor(z)] for z in Z)
		a = math.exp(0.6*math.log(100/M))
		self.draw_lines(lines, alpha = int(a*255), thickness= 1.0*a+0.7) 
		#self.draw_path(lines, alpha = 200, thickness= 0.5) 
		self.drw.flush()
		return pim

	def FF(self, z, t, k = 3, k1 = -5, k2 = 17):
		#k1 =  math.trunc(2*t) -7
		l =  0.5
		a =  0.4*sin(2*pi*t)
		b =  0.4*cos(2*pi*t)
		u = 0.4*cos(k*z) + a*cos(k1*z+2*pi*t) + b*cos(k2*z-2*pi*t) 
		v = 0.4*sin(k*z) + a*sin(k1*z+2*pi*t) + b*sin(k2*z-2*pi*t) 
		r = 1.0
		(x,y) = (u,v) #self.DiskToSqareMapping(u,v)
		return (self.width/2 + r*self.radius*x, self.height/2 + r*self.radius*y)	

	def DiskToSqareMapping(self, u, v):
		#print(u,v)
		c2 = 2*math.sqrt(2)
		a1 = 2 + u*u - v*v + c2*u
		a2 = 2 + u*u - v*v - c2*u
		b1 = 2 - u*u + v*v + c2*v
		b2 = 2 - u*u + v*v - c2*v
		#print(b1,b2)
		x = (math.sqrt(a1) - math.sqrt(a2))/2
		y = (math.sqrt(b1) - math.sqrt(b2))/2
		return (x,y)

	def draw_path(self, lines, alpha = 10, thickness = 0.5, color = "blue"):
		pf = lines[-1]
		for l in lines:
			pen = aggdraw.Pen(l[2], thickness, alpha)
			self.drw.line((pf[0][0], pf[0][1], l[0][0], l[0][1]), pen)
			pf = l

	def draw_lines(self, lines, alpha = 10, thickness = 0.5, color = "blue" ) :	
		pen = aggdraw.Pen("blue", thickness, alpha)
		for l in lines:
			#pen = aggdraw.Pen(l[2], thickness, alpha)
			self.drw.line((l[0][0], l[0][1], l[1][0], l[1][1]), pen)


	def draw_line(self,xy0, xy1):	
		pen = aggdraw.Pen("blue", 1.0, 10)
		self.drw.line((xy0[0], xy0[1], xy1[0], xy1[1]), pen)
		dot = aggdraw.Pen("blue", 1.0, 100)
		self.drw.line((xy0[0], xy0[1], xy0[0]+1, xy0[1]+1),dot)

	def GetColor(self, z):
		x = (self.COLORS_NUMBER) * z / (2*math.pi)
		return self.avg_clr(int(x), x - int(x))

	def avg_clr(self, i, d):
		c1 = self.Colors[i]
		c2=  self.Colors[(i+1)%self.COLORS_NUMBER]
		r = int(c1[0]*(1-d) + c2[0]*d)
		g = int(c1[1]*(1-d) + c2[1]*d)
		b = int(c1[2]*(1-d) + c2[2]*d)
		return (r,g,b)

	penIndex = 0
	count = 0
	def GetCairoClr(self):
		penIndex = (int)(self.penIndex / 25)
		d = self.penIndex / 25.0 - penIndex
		c1 = self.Colors[penIndex]
		c2=  self.Colors[penIndex+1]
		r = (c1[0]*(1-d) + c2[0]*d)/256
		g = (c1[1]*(1-d) + c2[1]*d)/256
		b = (c1[2]*(1-d) + c2[2]*d)/256
		return (r,g,b)
		

	def GetPen(self):
		self.penIndex += 1
		penIndex = (int)(self.penIndex / 25)
		d = self.penIndex / 25.0 - penIndex		
		return aggdraw.Pen(self.avg_clr(penIndex, d), 0.5, 80)
		

	def draw_dots(self,dots):	
		#pen = aggdraw.Pen("red", 0.5, 30)
		pen = aggdraw.Pen("blue", 1.0, 100)
		for d in dots:
			self.drw.rectangle((d[0], d[1], d[0]+1, d[1]+1), pen)

	def CreateLinearPattern(self, p):	
		linpat = cairo.LinearGradient(p[0][0],  p[0][1], p[1][0], p[1][1])
		d1 = math.dist(p[0],p[1])
		d2 = math.dist(p[2],p[3])
		#print(d1/d2)
		if d1>d2:
			linpat.add_color_stop_rgba(0.0, 0.0, 0.0, 1.0, 0.1)
			linpat.add_color_stop_rgba(1.0, 0.0, 0.0, 1.0, 0.3*d1/d2)
		else:
			linpat.add_color_stop_rgba(0.0, 0.0, 0.0, 1.0, 0.3*d2/d1)
			linpat.add_color_stop_rgba(1.0, 0.0, 0.0, 1.0, 0.1)		
		return linpat

	def draw_cr_lines(self, lines):
		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		for li in lines:
			self.context.move_to(li[0][0], li[0][1])
			self.context.line_to(li[1][0], li[1][1])		
			self.context.set_source_rgba(0.8, 0, 0, 0.1)
			self.context.set_line_width(2.0)
			self.context.stroke()
#
#	def poly(self, a, b):
#		line1 = LineString([a[0], a[1]]) 
#		line2 = LineString([b[0], b[1]]) 
#		p = line1.intersection(line2)
#			#print(p.x,p.y) 
#			pn = [a[0], b[0], (p.x, p.y) ,a[1], b[1]]
#		else:
#			pn = [a[0], a[1], b[1], b[0]]
#
#		return pn
#

	def draw_cr_test(self):
		for i in range(100):
			for j in range(3):
				self.context.rectangle( i*5.0, j*30.0, 500 - i*5, 25)
				self.context.set_source_rgba( 0, 0, 1.0, 0.05)
				self.context.fill()


	def CreateLinearPattern2(self, p):	
		x = (p[0][0] + p[1][0])/2
		y = (p[0][1] + p[1][1])/2
		linpat = cairo.LinearGradient(x,  y, p[2][0], p[2][1])
		linpat.add_color_stop_rgba(0.0, 0.0, 0.0, 1.0, 0.1)
		linpat.add_color_stop_rgba(0.7, 0.0, 0.0, 1.0, 0.2)
		linpat.add_color_stop_rgba(0.8, 0.0, 0.0, 1.0, 0.3)
		linpat.add_color_stop_rgba(1.0, 0.0, 0.0, 1.0, 0.9)
		return linpat

	def draw_cr_triangle(self, p):
		self.context.move_to(p[0][0], p[0][1])
		self.context.line_to(p[1][0], p[1][1])
		self.context.line_to(p[2][0], p[2][1])
		self.context.close_path()
		lp = self.CreateLinearPattern2(p)
		self.context.set_source(lp)
		self.context.fill()

	def draw_cr_polygons_triangle(self, lines):
		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		l = list(lines)
		x = 0.0
		dx = 1.0/len(l)
		#self.context.set_source_rgba(0.0, 0.0, 0.0, 1.0)					
		for i, j in zip(l[0::], l[-1::]+l[0::1]):
			
			p = self.poly(i,j)
			if len(p)>4:
				self.draw_cr_triangle(p[:3:])
				self.draw_cr_triangle([p[3],p[4],p[2]])
				self.context.set_source_rgba(1.0 , 0, 0.0, 0.1)
			else:
				self.context.move_to(p[0][0], p[0][1])
				self.context.line_to(p[1][0], p[1][1])
				#self.context.stroke()	
				self.context.line_to(p[2][0], p[2][1])	
				self.context.line_to(p[3][0], p[3][1])	
				#self.context.line_to(i[0][0], i[0][1])
				self.context.close_path()				
				self.context.set_source_rgba(0.0 , 0, 1.0, 0.1)	
				self.context.fill()
			x = x + 0
			#self.context.set_source_rgba(1.0 , 0, 0, 0.1)
			#self.context.stroke_preserve()
			#self.context.set_source_rgba(0.0 , 0, 1.0, 0.1)
			#lp = self.CreateLinearPattern(p)
			#self.context.set_source(lp)
			#self.context.fill()

		#self.context.move_to(l[0][0][0], l[0][0][1])
		#for li in l:
		#	self.context.line_to(li[0][0], li[0][1])
		#self.context.close_path()	
		#self.context.set_source_rgba(0.0, 0.0, 0.9, 1.0)
		#self.context.set_line_width(1.0)
		#self.context.stroke()			

	def draw_cr_polygons(self, lines):
		#self.context.rectangle(100, 50, 200 + t*100, 100 + t*100)
		l = list(lines)
		x = 0.0
		dx = 1.0/len(l)
		clr = self.GetCairoClr()
		self.context.set_operator(cairo.OPERATOR_OVER)
		#print(clr)
		#self.context.set_source_rgba(0.0, 0.0, 0.0, 1.0)					
		for i, j in zip(l[0::], l[-1::]+l[0::1]):		
			p = [i[0], i[1], j[1], j[0]]
			self.context.move_to(p[0][0], p[0][1])
			self.context.line_to(p[1][0], p[1][1])
			self.context.line_to(p[2][0], p[2][1])	
			self.context.line_to(p[3][0], p[3][1])	
			self.context.close_path()				
			self.context.set_source_rgba(clr[2], clr[1], clr[0], 0.1)	
			self.context.fill()
			self.context.move_to(p[0][0], p[0][1])
			self.context.line_to(p[1][0], p[1][1])
			self.context.set_line_width(0.95)
			self.context.set_source_rgba(clr[2], clr[1], clr[0], 0.1)
			self.context.stroke()


		self.context.fill()			



	def draw_polygons(self,lines):	
		pen = aggdraw.Pen("red",0.5, 0)
		l = list(lines)
		#for li in l:
		#	self.drw.line((li[0][0], li[0][1], li[1][0], li[1][1]), pen)
		br = aggdraw.Brush("red", 30)
		for i, j in zip(l[0::], l[-1::]+l[0::1]):
			p = aggdraw.Path([i[1][0], i[1][1], j[1][0], j[1][1], j[0][0], j[0][1], i[0][0], i[0][1]])
			self.drw.polygon(p, pen, br)
			#p = aggdraw.Path([j[0][0], j[0][1], j[1][0], j[1][1], i[0][0], i[0][1]])
			#self.drw.polygon(p, br)
		
	
