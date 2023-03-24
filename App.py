import tkinter as tk
from Views import CanvasView
from Views import ControlPanel

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
        },
        "max_colors_number" : {
            'name' : 'max_colors_number',
            'widget' : 'slider',
            'value' : 500,
            'type' : 'int',
            'label' : 'Max Colors Number',
            'interval' : [10, 1000, 1]
        },
        "colors_number" : {
            'name' : 'colors_number',
            'widget' : 'slider',
            'value' : 5,
            'type' : 'int',
            'label' : 'Colors Number',
            'interval' : [1, 1000, 1]
        },
        "colors_shift" : {
            'name' : 'colors_shift',
            'widget' : 'slider',
            'value' : 10,
            'type' : 'int',
            'label' : 'Colors Shift',
            'interval' : [1, 1000, 1]
        }          
        }

    def __init__(self, root):
        root.title("Wave Generator")

        root.minsize(800, 550)

        root.columnconfigure(0, weight=1)    
        root.rowconfigure(0, weight=1)

        cv = CanvasView(root, self.Parameters)
        cv.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=4)

        cp = ControlPanel(root, self.Parameters, cv)
        cp.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=4)