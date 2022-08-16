from SymView import SymView

class App:

    Parameters ={"Width": 900, "Height": 500}

    def __init__(self, root):
        root.title("Wave Generator")

        w = self.Parameters["Width"]
        h = self.Parameters["Height"]
        root.minsize(w, h)

        SymView(root)