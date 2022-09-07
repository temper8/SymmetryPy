import tkinter as tk
import math
import aggdraw
import random
import timeit

from PIL import Image, ImageDraw, ImageTk
from math import sin, cos, pi

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
		self.var = tk.DoubleVar(name = v['name'])
		self.var.trace_add('write', lambda var, indx, mode: self.update_var())
		label = tk.Label(master=self, text=v['label'])
		label.pack(side = 'top')		
		slider = tk.Scale( self, variable = self.var, orient = tk.HORIZONTAL, from_=v['interval'][0], to=v['interval'][1], resolution=v['interval'][2], length = 250 )
		slider.pack(anchor=tk.CENTER)


class SymView:

	#Parameters ={"Width": 720, "Height": 640, "Radius" : 350, "Time": 0.0, "Shift": 1.0}
	Vars = {}

	def __init__(self, root, parameters):
		self.Colors = self.GeneratePalette(5000)
		self.Parameters = parameters
		w = self.Parameters["Width"]
		h = self.Parameters["Height"]
		frame_a = tk.Frame(root)
		frame_b = tk.Frame(root)
		frame_a.grid(row=0, column=0)
		frame_b.grid(row=0, column=1)
		root.columnconfigure(0, weight=1)    
		root.rowconfigure(0, weight=1)

		self.canvas = tk.Canvas(frame_a, width=w, height=h)
		self.canvas.pack()

		self.saveFlag = tk.BooleanVar()
		self.saveFlag.set(0)
		chk1 = tk.Checkbutton(frame_b, text="Save",
                 variable=self.saveFlag,
                 onvalue=1, offvalue=0)
		chk1.pack(side = 'top')

		Slider(frame_b, parameters['Time'], self.Draw).pack()
		Slider(frame_b, parameters['Radius'], self.Draw).pack()



		self.label_fps = tk.Label(master=frame_b, text="fps")
		self.label_fps.pack(side = 'top')

		self.label_a = tk.Label(master=frame_b, text="time")
		self.label_a.pack(side = 'top')
		
		tk.Button(frame_b, text = " start ",  command = self.start).pack(side="top")
		tk.Button(frame_b, text = " stop ",  command = self.stop).pack(side="top")
		tk.Button(frame_b, text = " plus ",  command = self.plus).pack(side="top")
		tk.Button(frame_b, text = " Color palette ",  command = self.UpdatePalette).pack(side="top")
		
		#self.draw_init()
		
		self.RenderVar = tk.IntVar(name = "RenderType")
		self.Vars[self.RenderVar._name] = self.RenderVar
		self.RenderVar.set(0)
		tk.Radiobutton(frame_b, text="IggDraw", variable=self.RenderVar, value = 0, command=lambda : self.update()).pack(side="top")
		tk.Radiobutton(frame_b, text="Cairo", variable=self.RenderVar, value = 1, command=lambda : self.update()).pack(side="top")


		#self.spiro = Spiro(self.Parameters)  
		self.Draw()

	def update(self):
		t = self.ani_count/400
		#self.draw(t)

	def GeneratePalette(self, COLORS_NUMBER):
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

	def UpdatePalette(self):
		self.spiro.GeneratePalette()
		self.Draw()

	def Draw(self):
		pim = Render.SymmetryWall(self.Parameters, self.Vars, self.Colors)
		self.SaveImage(pim)
		self.photo = ImageTk.PhotoImage(pim)
		self.im = self.canvas.create_image(0,0, image=self.photo, anchor='nw')


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
	
