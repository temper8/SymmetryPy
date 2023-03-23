import tkinter as tk
import customtkinter as ctk
from App import App

if __name__ == '__main__':
    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
    root = ctk.CTk() 
    App(root)
    root.mainloop()