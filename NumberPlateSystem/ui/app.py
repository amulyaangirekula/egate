"""
Main application window
"""
import tkinter as tk
from tkinter import ttk
from NumberPlateSystem.config import DARK_BG

from NumberPlateSystem.ui.styles import setup_styles
from NumberPlateSystem.ui.frames.header_frame import HeaderFrame
from NumberPlateSystem.ui.frames.image_frame import ImageFrame
from NumberPlateSystem.ui.frames.results_frame import ResultsFrame
from NumberPlateSystem.ui.frames.button_frame import ButtonFrame

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Vehicle Access System")
        self.master.geometry("900x700")
        self.master.configure(bg=DARK_BG)
        
        # Setup styles
        setup_styles()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Create frames
        self.header = HeaderFrame(self.master)
        
        # Main content frame
        self.content_frame = ttk.Frame(self.master, style='TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for image
        self.left_panel = ttk.Frame(self.content_frame, style='TFrame')
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Right panel for results
        self.right_panel = ttk.Frame(self.content_frame, style='TFrame')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Image display
        self.image_frame = ImageFrame(self.left_panel)
        
        # Results display
        self.results_frame = ResultsFrame(self.right_panel)
        
        # Button controls
        self.button_frame = ButtonFrame(self.master, self)
        
        # Status bar
        self.status_bar = tk.Label(
            self.master, 
            textvariable=self.status_var, 
            relief=tk.RIDGE,     # More prominent relief style
            anchor=tk.W,
            bg="#333",           # Dark background for contrast
            fg="white",          # White text for readability
            font=("Segoe UI", 15, "bold"),  # Slightly bigger, bold font
            padx=15, 
            pady=10,              # More padding for better height
            bd=4,                # Border thickness for prominence
            highlightbackground="#00FFF5",  # Optional glowing border effect
            highlightthickness=1
        )


        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
        self.master.update_idletasks()
    
    def get_image_panel(self):
        """Get the image panel for operations"""
        return self.image_frame
    
    def get_results_panel(self):
        """Get the results panel for displaying information"""
        return self.results_frame