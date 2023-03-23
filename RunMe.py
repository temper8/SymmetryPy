import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from App import App

if __name__ == '__main__':
    root = ttk.Window(themename="superhero")
    App(root)
    root.mainloop()