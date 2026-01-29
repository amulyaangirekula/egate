"""
Smart Vehicle Access System - Entry Point
"""
import tkinter as tk
from ui.app import Application

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()