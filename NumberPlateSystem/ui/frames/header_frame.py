import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from NumberPlateSystem.config import DARK_BG, ACCENT, TEXT_COLOR

class HeaderFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, style='TFrame')
        self.frame.pack(fill=tk.X, pady=15)

        # Load college logo  (Fix it later)

        # logo_path = os.path.join("assets", "logo.png")  # Adjust path if needed
        # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        # logo_path = os.path.join(base_dir, "assets", "logo.png")
        
        
        # logo_image = Image.open(logo_path).resize((80, 80), Image.Resampling.LANCZOS)
        # self.logo = ImageTk.PhotoImage(logo_image)

        # # Logo on the left
        # self.logo_label = ttk.Label(self.frame, image=self.logo, style='TFrame')
        # self.logo_label.image = self.logo  # Keep reference
        # self.logo_label.pack(side=tk.LEFT, padx=(20, 10))

        # Text content next to logo
        self.text_frame = ttk.Frame(self.frame, style='TFrame')
        self.text_frame.pack(side=tk.LEFT, expand=True)

        # College name
        self.college_label = ttk.Label(
            self.text_frame,
            text="CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY (CBIT)",
            style='College.TLabel'
        )
        self.college_label.pack(pady=2)

        # Main title
        self.title_label = ttk.Label(
            self.text_frame, 
            text="AUTOMATIC NUMBER PLATE RECOGNITION", 
            style='Header.TLabel'
        )
        self.title_label.pack()

        # Subtitle
        self.subtitle_label = ttk.Label(
            self.text_frame, 
            text="Vehicle Access Control System",
            style='Subheader.TLabel'
        )
        self.subtitle_label.pack(pady=2)

        # Project ID
        self.project_info_label = ttk.Label(
            self.text_frame,
            text="Project ID: 01",
            style='Subheader.TLabel'
        )
        self.project_info_label.pack(pady=2)

        # Team Members
        self.team_label = ttk.Label(
            self.text_frame,
            text="Akshitha (001) | Amulya (003)",
            style='Subheader.TLabel'
        )
        self.team_label.pack(pady=2)
