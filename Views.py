import tkinter as tk
import math
import aggdraw
import random
import timeit

from PIL import Image, ImageDraw, ImageTk
from math import sin, cos, pi
import numpy as np

import Render

def my_callback(var, indx, mode):
	print(var)
	#print("Traced variable {}".format(var.get()))

class Slider(tk.Frame):

	def update_var(self):
		print(self.var.get())		
		self.variable['value'] = self.var.get()
		if self.call_back:
			self.call_back()

	def __init__(self, master, v, call_back) -> None:
		super().__init__(master)
		self.call_back = call_back
		self.variable = v
		if v['type'] =='double':
			self.var = tk.DoubleVar()
		else:
			self.var = tk.IntVar()			
		self.var.set(v['value'])
		self.var.trace_add('write', lambda var, indx, mode: self.update_var())
		v1 = v['interval'][1]
		v0 = v['interval'][0]		
		dv = v['interval'][2]
		slider = tk.Scale( self, 
		    variable = self.var, 
			orient = tk.HORIZONTAL,
            sliderlength = 20,
            width = 10,
            label=v['label'],		
	    	tickinterval= (v1-v0)/5,	 
			from_= v0, 
			to= v1, 
			resolution= dv, 
			length = 250 )
		slider.pack(anchor=tk.CENTER)


def avg_clr(c1, c2, d, alpha):
	r = int(c1[0]*(1-d) + c2[0]*d)
	g = int(c1[1]*(1-d) + c2[1]*d)
	b = int(c1[2]*(1-d) + c2[2]*d)
	return int.from_bytes(bytearray([r,g,b,alpha]), "big") 

class CanvasView(tk.Canvas):
	def __init__(self, master, parameters ) -> None:
		super().__init__(master)
		self.bind('<Configure>', self.resize)
		self.palette_generator = PaletteGenerator()
		self.Parameters = parameters
		self.palette = None

	def update_palette(self):
		self.palette_generator = PaletteGenerator()
		self.palette = None
		self.draw()

	def clear_palette(self):
		self.palette = None
		self.draw()

	def resize(self, event):
		print('canvas_resize')
		w = event.width
		h = event.height
		self.Parameters["Width"] = w 
		self.Parameters["Height"] = h		
		print (f'width  = {w}, height = {h}')		
		self.draw()

	def draw(self):
		if self.palette is None:
			pal_size = self.Parameters['colors_number']['value']
			pal_shift = self.Parameters['colors_shift']['value']
			self.palette = self.palette_generator.make_palette(pal_shift, pal_size)

		pim = Render.SymmetryWall(self.Parameters, self.palette)
		#self.SaveImage(pim)
		self.photo = ImageTk.PhotoImage(pim)
		self.create_image(0,0, image=self.photo, anchor='nw')

class PaletteGenerator():
	COLORS_NUMBER = 500
	def __init__(self) -> None:
		self.Colors = self.GeneratePalette(self.COLORS_NUMBER)

	def GeneratePalette(self, clrs_number):
		bi = 128.0/256
		Colors = []
		for i in range(0, clrs_number):
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
	
	def make_palette(self, clr_shift, clr_num):
		step = 50
		N = clr_num * step
		pal = np.zeros(N, dtype=np.uint32)
		clr = self.Colors[clr_shift:clr_shift+clr_num-1]
		clr.append(self.Colors[clr_shift])
		for i, (c1, c2) in enumerate(zip(clr, clr[-1:] + clr[:-1])):
			for j in range(0, step):
				d = float(j)/step
				pal[i*step+j] = avg_clr(c2,c1,d,225)
			#c2 = c1
		return pal	

class RadioSwitcher(tk.Frame):
	def __init__(self, master, items, command= None) -> None:
		super().__init__(master)
		self.command = command
		self.value = tk.StringVar()
		self.value.set(items[0])
		for item in items:
			tk.Radiobutton(self, text=item, variable=self.value, value= item, command= self.update).pack(side= tk.LEFT, padx=5)
	
	def update(self):
		print(self.value.get())
		if self.command:
			self.command()


class ControlPanel(tk.Frame):
	#Parameters ={"Width": 720, "Height": 640, "Radius" : 350, "Time": 0.0, "Shift": 1.0}
	Vars = {}

	def __init__(self, master, parameters, canvas_view) -> None:
		super().__init__(master)
		self.Parameters = parameters
		self.canvas_view = canvas_view



		Slider(self, parameters['Time'], self.canvas_view.draw).pack()
		Slider(self, parameters['Radius'], self.canvas_view.draw).pack()
		Slider(self, parameters['max_colors_number'], self.canvas_view.draw).pack()
		Slider(self, parameters['colors_number'], self.canvas_view.clear_palette).pack()		
		Slider(self, parameters['colors_shift'], self.canvas_view.clear_palette).pack()		

		self.label_fps = tk.Label(master=self, text="fps")
		self.label_fps.pack(side = 'top')

		self.label_a = tk.Label(master=self, text="time")
		self.label_a.pack(side = 'top')
		
		tk.Button(self, text = " start ",  command = self.start).pack(pady=5)
		tk.Button(self, text = " stop ",  command = self.stop).pack(pady=5)
		tk.Button(self, text = " plus ",  command = self.plus).pack(pady=5)
		tk.Button(self, text = " Color palette ",  command = self.canvas_view.update_palette).pack(pady=5)
		
		rs = RadioSwitcher(self, ['IggDraw','Cairo'], command= self.update)
		rs.pack(pady=5)

		self.save_flag = tk.BooleanVar()
		self.save_flag.set(0)
		chk1 = tk.Checkbutton(self, text="Save",
                 variable=self.save_flag,
                 onvalue=1, offvalue=0)
		chk1.pack(side = 'top')
		#self.spiro = Spiro(self.Parameters)  
		self.canvas_view.draw()

	def update(self):
		t = self.ani_count/400
		#self.draw(t)

	def SaveImage(self, pim):
		if self.saveFlag.get():
			fn = "tmp\\{0:05d}.png".format(self.ani_count)
			print(fn)
			pim.save(fn, "PNG")

	ani_count = 0
	stop_flag = False

	fc = 0
	fps = 0
	start_time = 0
	def FPS(self):
		if self.fc == 0 :
			self.start_time = timeit.default_timer()
		self.fc = self.fc + 1
		if self.fc>10:
			dt = timeit.default_timer() - self.start_time
			self.fps = self.fc / dt
			self.fc = 0
		self.label_fps["text"] = "fps = " + "{:5.2f}".format(self.fps)	
		

	def animate(self):
		self.FPS()
		t = self.ani_count/1000
		self.Vars["Time"].set(t)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)
		self.ani_count +=  1
		if not self.stop_flag and (self.ani_count<1000):
			self.canvas.after(10, self.animate) 

	def start(self):
		self.stop_flag = False
		self.ani_count = 0
		self.animate()

	def plus(self):
		self.stop_flag = False
		self.ani_count += 1
		t = self.Vars["Time"].get() + 0.01
		self.Vars["Time"].set(t)
		self.label_a["text"] = "t = " + "{:5.3f}".format(t)

	def stop(self):
		self.stop_flag = True


	def Slider1Moved(self, v):
		#self.Parameters["Time"] = int(v)/100.0
		self.DrawEx()
		#self.label_a["text"] = "t = " + "{:5.3f}".format(self.Parameters["Time"])	

	def Slider2Moved(self, v):
		#self.Parameters["Shift"] = int(v)/150.0
		self.DrawEx()
		#self.label_a["text"] = "t = " + "{:5.3f}".format(self.Parameters["Time"])	
	
