"""
UI styles for the application
"""
from tkinter import ttk
from config import DARK_BG, LIGHT_BG, ACCENT, TEXT_COLOR, BTN_BG

def setup_styles():
    """Configure the application styles"""
    style = ttk.Style()
    style.theme_use('default')
    
    # Frame styles
    style.configure('TFrame', background=DARK_BG)
    
    # Button styles
    style.configure('TButton', 
                    background=BTN_BG, 
                    foreground=TEXT_COLOR, 
                    borderwidth=0,
                    focuscolor=ACCENT,
                    font=('Segoe UI', 10, 'bold'))
    style.map('TButton', 
              background=[('active', ACCENT)],
              foreground=[('active', DARK_BG)])
    
    # Label styles
    style.configure('TLabel', 
                    background=DARK_BG, 
                    foreground=TEXT_COLOR,
                    font=('Segoe UI', 11))
    
    # Header label style
    style.configure('Header.TLabel', 
                    font=('Segoe UI', 18, 'bold'),
                    foreground=ACCENT)
    
    style.configure('College.TLabel', 
                    font=('Helvetica', 12, 'bold'),
                    foreground=ACCENT, 
                    background=DARK_BG)
    


    # Subheader label style
    style.configure('Subheader.TLabel', 
                    font=('Segoe UI', 12))
    
    # Results header style
    style.configure('ResultsHeader.TLabel',
                    font=('Segoe UI', 12, 'bold'),
                    foreground=ACCENT)
    
    # Status bar style  
    style.configure('TLabel',
                    background=LIGHT_BG,
                    foreground=TEXT_COLOR)