import Views 
import tkinter as tk

class App:

    Parameters ={
        "Width": 800, 
        "Height": 700,
        "Radius" : {
            'name' : 'radius',
            'widget' : 'slider',
            'value' : 1.0,
            'type' : 'double',
            'label' : 'Radius',
            'interval' : [1.0, 10.0, 0.1]
        },
        "Shift": {
            'value' : 1.0
        },
        "Time" : {
            'name' : 'time',
            'widget' : 'slider',
            'value' : 0.0,
            'type' : 'double',
            'label' : 'Time',
            'interval' : [0.0, 1.0, 0.01]
        }
        }

    def __init__(self, root):
        root.title("Wave Generator")

        #w = self.Parameters["Width"]
        #h = self.Parameters["Height"]
        root.minsize(800, 550)
        root.columnconfigure(0, weight=1)    
        root.rowconfigure(0, weight=1)
        cv = Views.CanvasView(root, self.Parameters)
        cv.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=4)

        mv = Views.ControlPanel(root, self.Parameters, cv)
        mv.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=4)