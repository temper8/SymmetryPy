from SymView import SymView

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
        root.minsize(800, 450)

        SymView(root, self.Parameters)