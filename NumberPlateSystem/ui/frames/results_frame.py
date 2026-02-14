# Results display panel
import tkinter as tk
from tkinter import ttk, scrolledtext
from NumberPlateSystem.config import LIGHT_BG, TEXT_COLOR

class ResultsFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, style='TFrame')
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title
        self.title_label = ttk.Label(
            self.frame, 
            text="RECOGNITION RESULTS", 
            style='ResultsHeader.TLabel'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Results text box
        self.response_frame = ttk.Frame(self.frame, style='TFrame')
        self.response_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.response_box = scrolledtext.ScrolledText(
            self.response_frame, 
            wrap=tk.WORD, 
            width=45, 
            height=12,
            font=('Segoe UI', 12),  # Changed font for modern feel
            bg=LIGHT_BG,           
            fg="white",             # White text for readability
            insertbackground="white",  # White cursor for contrast
            borderwidth=2,          # Subtle border
            relief=tk.SOLID,        # Solid border for neatness
            padx=15,                # Padding for content
            pady=10,                # Padding for content
            state=tk.DISABLED       # Make the text box non-editable
        )
        self.response_box.pack(fill=tk.BOTH, expand=True)
        
    def display_text(self, text):
        """Display text in the results box"""
        self.response_box.config(state=tk.NORMAL)  # Allow text update temporarily
        self.response_box.delete("1.0", tk.END)
        self.response_box.insert(tk.END, text)
        self.response_box.config(state=tk.DISABLED)  # Set it back to non-editable
        
    def append_text(self, text):
        """Append text to the results box"""
        self.response_box.config(state=tk.NORMAL)  # Temporarily enable editing
        self.response_box.insert(tk.END, text)
        self.response_box.config(state=tk.DISABLED)  # Set back to non-editable
        
    def clear(self):
        """Clear the results box"""
        self.response_box.config(state=tk.NORMAL)  # Temporarily enable editing
        self.response_box.delete("1.0", tk.END)
        self.response_box.config(state=tk.DISABLED)  # Set back to non-editable
