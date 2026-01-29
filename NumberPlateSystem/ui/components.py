"""
Custom UI components
"""
import tkinter as tk
from config import BTN_BG, TEXT_COLOR, ACCENT, DARK_BG

class HoverButton(tk.Button):
    """Button with hover effect"""
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = ACCENT
        self["foreground"] = DARK_BG

    def on_leave(self, e):
        self["background"] = self.defaultBackground
        self["foreground"] = TEXT_COLOR